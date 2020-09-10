from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^request', views.create_request),
    url(r'^workrequests', views.work_requests),
    url(r'^myrequests', views.my_requests),
    url(r'^myrequest_update', views.my_request_update)
]
