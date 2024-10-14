from django.shortcuts import get_object_or_404, render, redirect

from main.models import Sitio
# from django.db.models import Max
# from django.views.generic import ListView
from .forms import ImagesForm
from .models import Imagen, Comentario
# from django.utils import timezone
from django.contrib import messages
from django.db.models import DateField
from django.db.models.functions import Trunc
from collections import OrderedDict
# from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from .serializers import GaleriaSerializer
# from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


# class GaleriaListView(ListView):

@login_required(login_url='login/')
def fileupload(request):
    if request.method == 'POST':
        print("#######################")
        print(request.user)
        form = ImagesForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            sitio = form.cleaned_data['sitio']
            comentario_texto = form.cleaned_data['comentario']
            fecha_carga = form.cleaned_data['fecha_carga']
            # Obtener todas las imágenes
            imagenes = request.FILES.getlist('imagenes')
            imagenes_a_crear = [
                Imagen(imagen=image, sitio=sitio,
                       fecha_carga=fecha_carga,
                       usuario=request.user) for image in imagenes
                ]

            # Usar bulk_create para mejorar la eficiencia
            Imagen.objects.bulk_create(imagenes_a_crear)

            # Crear y guardar el comentario si existe alguno
            if comentario_texto:  # Si hay algún comentario para guardar
                Comentario.objects.create(
                    sitio=sitio,
                    comentario=comentario_texto,
                    fecha_carga=fecha_carga,
                    usuario=request.user
                    )

            # Añadir un mensaje de éxito
            messages.success(request, "Imágenes cargadas correctamente.")
            return redirect('home_page')  # Redirigir a la página de éxito
        else:
            messages.error(request,
                           """Se encontraron errores en el formulario,
                           por favor corrígelos.""")
            return render(request, "cargar.html", {'form': form})
    else:
        form = ImagesForm(user=request.user)
    return render(request, 'cargar.html', {'form': form})


def display_images_comments(request, site_id):
    # Obtener el sitio o mostrar un 404 si no existe
    sitio = get_object_or_404(Sitio, id=site_id)
    imagenes = Imagen.objects.filter(sitio=sitio).annotate(fecha=Trunc(
        'fecha_carga',
        'day',
        output_field=DateField())).order_by('-fecha')

    comentarios = Comentario.objects.filter(sitio=sitio).annotate(fecha=Trunc(
        'fecha_carga',
        'day',
        output_field=DateField())).order_by('-fecha')

    comentarios_data = []

    for comentario in comentarios:
        usuario = comentario.usuario
        # Asumimos que el cargo está almacenado en un perfil relacionado
        # Accede al primer perfil de usuario o maneja la ausencia del mismo
        user_profile = usuario.userprofile_set.first() if usuario else None

        # Accede al cargo del usuario si el perfil existe
        cargo_usuario = user_profile.cargo if user_profile else ''

        es_prevencionista = cargo_usuario == 'PRE'

        usuario_nombre = (
            f"{usuario.first_name} {usuario.last_name}"
            if usuario else "Usuario desconocido"
            )
        comentarios_data.append({
            'comentario': comentario.comentario,
            'usuario': usuario_nombre,
            'fecha': comentario.fecha.strftime('%Y-%m-%d'),
            'es_prevencionista': es_prevencionista
        })

    items_por_fecha = OrderedDict()

    # Agregar imágenes
    for imagen in imagenes:
        # Asegúrate de usar el mismo formato
        fecha_key = imagen.fecha.strftime('%Y-%m-%d')
        if fecha_key not in items_por_fecha:
            items_por_fecha[fecha_key] = {'imagenes': [], 'comentarios': []}
        items_por_fecha[fecha_key]['imagenes'].append(imagen)

    # Agregar comentarios desde comentarios_data
    for comentario in comentarios_data:
        # La fecha ya está en el formato correcto
        fecha_key = comentario['fecha']
        if fecha_key not in items_por_fecha:
            items_por_fecha[fecha_key] = {
                'imagenes': [],
                'comentarios': [],
                'prevencionista': False}

        items_por_fecha[fecha_key]['comentarios'].append(comentario)
        # Actualizar la bandera de prevencionista si es necesario
        if comentario['es_prevencionista']:
            items_por_fecha[fecha_key]['prevencionista'] = True

    context = {
        'sitio': sitio,
        'items_por_fecha': items_por_fecha,
    }

    return render(request, 'images_comments.html', context)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    # Redirige a los usuarios ya autenticados
    redirect_authenticated_user = True
    next_page = reverse_lazy('galeria:load_images')


# class UltimasImagenes(APIView):
#     def get(self, request, slug_sitio):
#         galeria = get_object_or_404(Galeria, slug=slug_sitio)
#         serializer = GaleriaSerializer(galeria, context={'request': request})
#         return Response(serializer.data)
