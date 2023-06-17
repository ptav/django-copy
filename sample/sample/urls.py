"""sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from message.views import message_test, message_test_phase2
from modal.views import modal_test
from djangocopy.views import index

urlpatterns = [
    path('', index),
    path('message-test', message_test, name='message-test'),
    path('message-test-phase2', message_test_phase2, name='message-test-phase2'),
    path('modal-test', modal_test, name='modal-test'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('filer/', include('filer.urls')),
    path('copy/', include('djangocopy.urls')),

    path('admin/', admin.site.urls),
]
