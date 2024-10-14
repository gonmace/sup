from django.urls import path
from . import views

app_name = 'main'  # Definir el namespace 'main'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('get_site_data/', views.get_site_data, name='get_site_data'),
    path('get_full_site_data/',
         views.get_full_site_data, name='get_full_site_data'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]
