from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^sensor', views.index, name='index'),
    url(r'^today', views.today, name='today')
]
