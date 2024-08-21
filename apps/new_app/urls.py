from django.urls import re_path

from apps.new_app import views

urlpatterns = (re_path(r"^test/$", views.test),)
