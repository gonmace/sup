# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<int:sitio_pk>/',
         views.render_streamfield,
         name='render_streamfield'
         ),
]
