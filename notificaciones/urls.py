from django.urls import path
from . import views


app_name = 'notificaciones'

urlpatterns = [
     path(
          'firebase-messaging-sw.js',
          views.service_worker,
          name='service_worker'
          ),
     path('save_token/', views.save_token, name='save_token'),
     path('firebase-logo.png', views.firebase_logo, name='firebase-logo'),
]
