import os.path
import sys
import re
import warnings
import cx_Oracle


from django.db import connection, models
from django.db.backends.util import truncate_name
from django.core.management.color import no_style
from django.db.models.fields import NOT_PROVIDED
from django.db.utils import DatabaseError

# In revision r16016 function get_sequence_name has been transformed into
# method of DatabaseOperations class. To make code backward-compatible we
# need to handle both situations.
try:
    from django.db.backends.oracle.base import get_sequence_name\
        as original_get_sequence_name
except ImportError:
    original_get_sequence_name = None

from south.db import generic

warnings.warn("! WARNING: South's Oracle support is still alpha. "
              "Be wary of possible bugs.")

class DatabaseOperations(generic.DatabaseOperations):    
    """
    Oracle implementation of database operations.    
    """
    backend_name = 'oracle'

    alter_string_set_type =     'ALTER TABLE %(table_name)s MODIFY %(column)s %(type)s %(nullity)s;'
    alter_string_set_default =  'ALTER TABLE %(table_name)s MODIFY %(column)s DEFAULT %(default)s;'
    add_column_string =         'ALTER TABLE %s ADD %s;'
    delete_column_string =      'ALTER TABLE %s DROP COLUMN %s;'
    add_constraint_string =     'ALTER TABLE %(table_name)s ADD CONSTRAINT %(constraint)s %(clause)s'

    allows_combined_alters = False
    
    constraints_dict = {
        'P': 'PRIMARY KEY',
        'U': 'UNIQUE',
        'C': 'CHECK',
        'R': 'FOREIGN KEY'
    }

    def get_sequence_name(self, table_name):
        if original_get_sequence_name is None:
            return self._get_connection().ops._get_sequence_name(table_name)
        else:
            return original_get_sequence_name(table_name)

    def adj_column_sql(self, col):
        # Fix boolean field values: need to be 1/0, not True/False
        col = re.sub('DEFAULT True', 'DEFAULT 1', col)
        col = re.sub('DEFAULT False', 'DEFAULT 0', col)
        # Fix other things
        col = re.sub('(?P<constr>CHECK \(.*\))(?P<any>.*)(?P<default>DEFAULT \d+)', 
                     lambda mo: '%s %s%s'%(mo.group('default'), mo.group('constr'), mo.group('any')), col) #syntax fix for boolean/integer field only
        col = re.sub('(?P<not_null>(NOT )?NULL) (?P<misc>(.* )?)(?P<default>DEFAULT.+)',
                     lambda mo: '%s %s %s'%(mo.group('default'),mo.group('not_null'),mo.group('misc') or ''), col) #fix order of NULL/NOT NULL and DEFAULT
        return col

    def check_meta(self, table_name):
        return table_name in [ m._meta.db_table for m in models.get_models() ] #caching provided by Django
    
    def normalize_name(self, name):
        """
        Get the properly shortened and uppercased identifier as returned by quote_name(), but without the actual quotes.
        """
        nn = self.quote_name(name)
        if nn[0] == '"' and nn[-1] == '"':
            nn = nn[1:-1]
        return nn

    @generic.invalidate_table_constraints
    def create_table(self, table_name, fields): 
        qn = self.quote_name(table_name)
        columns = []
        autoinc_sql = ''

        for field_name, field in fields:
            col = self.column_sql(table_name, field_name, field)
            if not col:
                continue
            col = self.adj_column_sql(col)

            columns.append(col)
            if isinstance(field, models.AutoField):
                autoinc_sql = connection.ops.autoinc_sql(table_name, field_name)

        sql = 'CREATE TABLE %s (%s);' % (qn, ', '.join([col for col in columns]))
        self.execute(sql)
        if autoinc_sql:
            self.execute(autoinc_sql[0])
            self.execute(autoinc_sql[1])

    @generic.invalidate_table_constraints
    def delete_table(self, table_name, cascade=True):
        qn = self.quote_name(table_name)

        # Note: PURGE is not valid syntax for Oracle 9i (it was added in 10)
        if cascade:
            self.execute('DROP TABLE %s CASCADE CONSTRAINTS;' % qn)
        else:
            self.execute('DROP TABLE %s;' % qn)
        
        # If the table has an AutoField a sequence was created.
        sequence_sql = """
DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = '%(sq_name)s' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 1 THEN
        EXECUTE IMMEDIATE 'DROP SEQUENCE "%(sq_name)s"';
    END IF;
END;
/""" % {'sq_name': self.get_sequence_name(table_name)}
        self.execute(sequence_sql)

    @generic.invalidate_table_constraints
    def alter_column(self, table_name, name, field, explicit_name=True):
        qn = self.quote_name(table_name)

        # hook for the field to do any resolution prior to it's attributes being queried
        if hasattr(field, 'south_init'):
            field.south_init()
        field = self._field_sanity(field)

        # Add _id or whatever if we need to
        field.set_attributes_from_name(name)
        if not explicit_name:
            name = field.column
        qn_col = self.quote_name(name)

        # First, change the type
        # This will actually also add any CHECK constraints needed,
        # since e.g. 'type' for a BooleanField is 'NUMBER(1) CHECK (%(qn_column)s IN (0,1))'
        params = {
            'table_name':qn,
            'column': qn_col,
            'type': self._db_type_for_alter_column(field),
            'nullity': 'NOT NULL',
            'default': 'NULL'
        }
        if field.null:
            params['nullity'] = 'NULL'

        if not field.null and field.has_default():
            params['default'] = field.get_default()

        sql_templates = [
            (self.alter_string_set_type, params),
            (self.alter_string_set_default, params.copy()),
        ]

        # UNIQUE constraint
        unique_constraint = list(self._constraints_affecting_columns(table_name, [name], 'UNIQUE'))
        if field.unique and not unique_constraint:
            self.create_unique(table_name, [name])
        elif not field.unique and unique_constraint:
            self.delete_unique(table_name, [name])

        # drop CHECK constraints. Make sure this is executed before the ALTER TABLE statements
        # generated above, since those statements recreate the constraints we delete here.
        check_constraints = self._constraints_affecting_columns(table_name, [name], "CHECK")
        for constraint in check_constraints:
            self.execute(self.delete_check_sql % {
                'table': self.quote_name(table_name),
                'constraint': self.quote_name(constraint),
            })

        for sql_template, params in sql_templates:
            try:
                self.execute(sql_template % params)
            except DatabaseError, exc:
                description = str(exc)
                # Oracle complains if a column is already NULL/NOT NULL
                if 'ORA-01442' in description or 'ORA-01451' in description:
                    # so we just drop NULL/NOT NULL part from target sql and retry
                    params['nullity'] = ''
                    sql = sql_template % params
                    self.execute(sql)
                else:
                    raise

    @generic.copy_column_constraints
    @generic.delete_column_constraints
    def rename_column(self, table_name, old, new):
        if old == new:
            # Short-circuit out
            return []
        self.execute('ALTER TABLE %s RENAME COLUMN %s TO %s;' % (
            self.quote_name(table_name),
            self.quote_name(old),
            self.quote_name(new),
        ))

    @generic.invalidate_table_constraints
    def add_column(self, table_name, name, field, keep_default=True):
        sql = self.column_sql(table_name, name, field)
        sql = self.adj_column_sql(sql)

        if sql:
            params = (
                self.quote_name(table_name),
                sql
            )
            sql = self.add_column_string % params
            self.execute(sql)

            # Now, drop the default if we need to
            if not keep_default and field.default is not None:
                field.default = NOT_PROVIDED
                self.alter_column(table_name, name, field, explicit_name=False)

    def delete_column(self, table_name, name):
        return super(DatabaseOperations, self).delete_column(self.quote_name(table_name), name)

    def lookup_constraint(self, db_name, table_name, column_name=None):
        if column_name:
            # Column names in the constraint cache come from the database,
            # make sure we use the properly shortened/uppercased version
            # for lookup.
            column_name = self.normalize_name(column_name)
        return super(DatabaseOperations, self).lookup_constraint(db_name, table_name, column_name)

    def _constraints_affecting_columns(self, table_name, columns, type="UNIQUE"):
        if columns:
            columns = [self.normalize_name(c) for c in columns]
        return super(DatabaseOperations, self)._constraints_affecting_columns(table_name, columns, type)

    def _field_sanity(self, field):
        """
        This particular override stops us sending DEFAULTs for BooleanField.
        """
        if isinstance(field, models.BooleanField) and field.has_default():
            field.default = int(field.to_python(field.get_default()))
        return field

    def _fill_constraint_cache(self, db_name, table_name):
        self._constraint_cache.setdefault(db_name, {}) 
        self._constraint_cache[db_name][table_name] = {} 

        rows = self.execute("""
            SELECT user_cons_columns.constraint_name,
                   user_cons_columns.column_name,
                   user_constraints.constraint_type
            FROM user_constraints
            JOIN user_cons_columns ON
                 user_constraints.table_name = user_cons_columns.table_name AND 
                 user_constraints.constraint_name = user_cons_columns.constraint_name
            WHERE user_constraints.table_name = '%s'
        """ % self.normalize_name(table_name))

        for constraint, column, kind in rows:
            self._constraint_cache[db_name][table_name].setdefault(column, set())
            self._constraint_cache[db_name][table_name][column].add((self.constraints_dict[kind], constraint))
        return
