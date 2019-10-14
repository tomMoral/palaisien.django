from django.urls import path, re_path

from . import views

urlpatterns = [
    path('<int:seminar_id>/', views.register, name='register'),
    re_path(r'^[^/]*/?$', views.index, name='index'),
    # url(r'^CV/pyparis17.*$', 'django.contrib.staticfiles.views.serve', kwargs={
    #     'path': 'CV/pyparis17/index.html',
    #     'document_root': settings.STATIC_ROOT}),
]
