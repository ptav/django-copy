from django.urls import path

from .views import static_page, index



app_name = 'djangocopy'

urlpatterns = [
    path('<str:slug>/',static_page,name='static'),
    path('', index),
]
