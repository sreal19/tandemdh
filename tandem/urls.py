__author__ = 'sbr'

from django.conf.urls import patterns, url

from tandem import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
  #  url(r'getproject/$',views.getproject, name='getproject'),
    url(r'getinput/$',views.getinput, name='getinput'),
    url(r'analyze/$',views.analyze, name='analyze'),
    url(r'results/$',views.results, name='results')
   # url(r'runengine/$',views.runengine, name='runengine')
)