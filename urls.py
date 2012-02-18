from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'istweb.home.views.index', name='root'),
    url(r'^contacts/', include('istweb.contacts.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'users/login.html' }),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^recommendation/', include('istweb.recommendation.urls')),

    url(r'^admin/auth/user/bulkadd/$', 'users.views.bulkadd', name='users_bulkadd'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
