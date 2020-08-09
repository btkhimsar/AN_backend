from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^languages', views.add_language),
    url(r'^createlanguage', views.create_language),
    url(r'^languagedata', views.language_data)
]
