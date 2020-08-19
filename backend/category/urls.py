from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories', views.super_category_list),
    url(r'^subcategory', views.handle_category),
    url(r'^category', views.handle_super_category),
    url(r'^questions', views.questions)
]
