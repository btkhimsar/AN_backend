from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^request', views.job),
    url(r'^workrequests', views.work_requests),
    url(r'^myrequests', views.my_request),
    url(r'^myrequest_update', views.my_request_update)
]
