from django.conf import settings
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^[^/]*$', views.index, name='index'),
    # url(r'^CV/pyparis17.*$', 'django.contrib.staticfiles.views.serve', kwargs={
    #     'path': 'CV/pyparis17/index.html',
    #     'document_root': settings.STATIC_ROOT}),
]
