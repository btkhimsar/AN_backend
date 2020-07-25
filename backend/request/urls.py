from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^request', views.job),
    url(r'^workrequests', views.work_requests),
    url(r'^myrequest', views.my_request)
]
