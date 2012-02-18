from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('contacts.views',
    url(r'^$', 'index', name='contacts_index'),
    url(r'^upload/$', 'upload', name='contacts_upload'),
    url(r'^edit/$', 'edit', name='contacts_edit'),
    url(r'^me/$', 'me', name='contacts_me'),
    url(r'^(?P<username>[A-Za-z0-9\-_]+)/$', 'show', name='contacts_show'),
)

