import os
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve

from .views import static_page, index


def unprotected_serve(request, path):
    "Serve django-copy templates and images without user restrictions that may be imposed on MEDIA_URL"
    return serve(request, path, settings.MEDIA_ROOT, True)



urlpatterns = [
    path('<str:slug>/',static_page,name='static'),
    path('', index),
]

# If DEBUG is False, the MEDIA_URL/djangocopy/* urls are not served by Django
#if settings.DEBUG:
#    urlpatterns += [
#        #re_path(r'^%sdjangocopy/(?P<path>.*)$' % settings.MEDIA_URL[1:], unprotected_serve, {'document_root': settings.MEDIA_ROOT}),
#        re_path(r'^{}/(?P<path>.*)$'.format(settings.DJANGOCOPY_IMAGE_ROOT[1:]), unprotected_serve),
#    ]