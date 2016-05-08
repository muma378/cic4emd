from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^images/browse', views.browse, name='browse'),
    url(r'^images/upload', views.upload, name='upload')
]
