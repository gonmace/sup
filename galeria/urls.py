from django.urls import path
from . import views


app_name = 'galeria'

urlpatterns = [
    # path('', GaleriaListView.as_view(), name='galeria_list'),
    # path('cargar/login/', CustomLoginView.as_view(), name='login'),
    path('cargar/', views.fileupload, name='load_images'),
    path('<int:site_id>/',
         views.display_images_comments, name='images_comments'),

]
