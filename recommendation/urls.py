from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('recommendation.views',
        url(r'^$', 'index', name='recommendation_index'),
      )

