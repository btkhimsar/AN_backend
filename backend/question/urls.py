from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add_question', views.add_question),
    url(r'^add_answer', views.add_answer),
    url(r'^add_subquestion', views.add_sub_question),
    url(r'^add_subanswer', views.add_sub_answer),
    url(r'^questions', views.questions)
]
