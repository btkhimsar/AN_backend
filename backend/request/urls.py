from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^request', views.create_request),
    url(r'^workrequests', views.work_requests),
    url(r'^myrequests', views.my_requests),
    url(r'^my_request_details', views.my_request_details),
    url(r'^completed_request', views.request_completion),
    url(r'^send_interest', views.send_interest),
    url(r'^interestssent', views.interests_sent),
    url(r'^markasspam', views.mark_as_spam)
]
