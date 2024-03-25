from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from . import views

urlpatterns = [
    path('register/<int:seminar_id>/', views.register, name='register'),
    re_path(r'^[^/]*/?$', views.index, name='index'),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('programme/images/favicon.png')
    ))
]
