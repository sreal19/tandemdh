from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.core.files.storage import FileSystemStorage
import os, time
from tandem import views
from TandemDH import settings


urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'project/$',views.project, name='project'),
    url(r'upload/$',views.upload, name='upload'),
    url(r'analyze/$',views.analyze, name='analyze'),
    url(r'results/$',views.results, name='results'),
    url(r'download/$',views.download, name='download'),
    url(r'about/$',views.about, name='about'),
    url(r'documentation/$',views.documentation, name='documentation'),
    url(r'sample/$',views.sample, name='sample'),
    url(r'terms/$',views.terms, name='terms'),
    url(r'team/$',views.team, name='team'),
    url(r'^tandem/', include('tandem.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'index/$',views.index, name='index'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)






