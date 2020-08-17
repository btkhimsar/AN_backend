from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.login),
    url(r'^auth', views.auth),
    url(r'^update_profile', views.update_profile),
    url(r'^profile', views.profile),
    url(r'^notification', views.notification)
]
