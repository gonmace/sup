from django.urls import path
from . import views


app_name = 'main'  # Definir el namespace 'main'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('get_site_data/', views.get_site_data, name='get_site_data'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('get_chats/<int:site_id>/<int:cant>',
         views.get_chats,
         name='get_chats'),

]
