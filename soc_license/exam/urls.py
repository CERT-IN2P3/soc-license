from django.urls import path, re_path

from . import views

urlpatterns = [
    path("questions/", views.questions, name='questions'),
    re_path(r'questions/(?P<question>[\w]+)', views.answer, name='answer'),
    path("init/", views.init, name='init')
]