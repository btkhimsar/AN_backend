from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories', views.categories),
    url(r'^category', views.create_category),
    url(r'^super_category', views.create_super_category)
]
