# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Book'
        db.create_table('recommendation_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('book_author', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('book_img_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('book_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('book_recommender', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('recommendation', ['Book'])

    def backwards(self, orm):
        # Deleting model 'Book'
        db.delete_table('recommendation_book')

    models = {
        'recommendation.book': {
            'Meta': {'object_name': 'Book'},
            'book_author': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'book_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'book_img_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'book_recommender': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'book_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['recommendation']