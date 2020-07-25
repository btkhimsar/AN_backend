from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories', views.category_list),
    url(r'^subcategory', views.handle_subcategory),
    url(r'^category', views.handle_category)
]
