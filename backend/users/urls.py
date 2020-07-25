from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.login),
    url(r'^auth', views.auth),
    url(r'^profile', views.profile)
]
