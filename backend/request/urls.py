from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^request', views.create_request),
    url(r'^workrequests', views.work_requests),
    url(r'^myrequests', views.my_requests),
    url(r'^getrequestdetails', views.get_request_details),
    url(r'^markrequestcomplete', views.request_completion),
    url(r'^send_interest', views.send_interest),
    url(r'^sentinterests', views.interests_sent),
    url(r'^markrequestasspam', views.mark_request_as_spam)
]
