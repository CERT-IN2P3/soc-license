from django.urls import path, re_path

from . import views

urlpatterns = [
    path('csrf', views.csrf, name='csrf')
]
