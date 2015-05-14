__author__ = 'sbr'

from django.conf.urls import patterns, url

from tandem import views

urlpatterns = patterns('',
    url(r'analyze/$',views.analyze, name='analyze'),
    url(r'results/$',views.results, name='results'),
    url(r'upload/$',views.upload, name='upload'),
    url(r'project/$',views.project, name='project'),
    url(r'download/$',views.download, name='download'),
    url(r'about/$',views.about, name='about'),
    url(r'documentation/$',views.documentation, name='documentation'),
    url(r'sample/$',views.sample, name='sample'),
    url(r'terms/$',views.terms, name='terms'),
    url(r'team/$',views.team, name='team'),
)
