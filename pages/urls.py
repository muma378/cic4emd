from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<category_abbr>\w+)/$', views.category_archive, name='category'),
    url(r'^(?P<category_abbr>\w+)/(?P<publishment_id>\d+)/$', views.publishment, name='publishment'),    
    url(r'^images/browse', views.browse, name='browse'),
    url(r'^images/upload', views.upload, name='upload')
]
