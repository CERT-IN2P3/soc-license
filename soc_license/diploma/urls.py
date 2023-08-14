from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'(?P<uuid>[\w-]+)\.(?P<format>[\w]+)', views.diploma_view, name='diploma_view')
]
