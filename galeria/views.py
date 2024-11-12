from django.shortcuts import get_object_or_404, render, redirect

from main.models import Sitio
from .forms import ImagesForm
from .models import Imagen, Comentario
from django.contrib import messages
from django.db.models.functions import TruncMinute
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import os
from PIL import Image


def convert_to_webp(image):
    if image.imagen:
        original_path = image.imagen.path
        webp_path = f"{original_path.rsplit('.', 1)[0]}.webp"

        # Comprobar si el archivo WebP ya existe
        if not os.path.exists(webp_path):
            img = Image.open(original_path)
            img.save(webp_path, "WEBP", quality=50)
            return f'Guardada WebP: {webp_path}'
        else:
            return f'Archivo WebP ya existe: {webp_path}'


@login_required(login_url='login/')
def fileupload(request):
    if request.method == 'POST':
        form = ImagesForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            sitio = form.cleaned_data['sitio']
            comentario_texto = form.cleaned_data['comentario']
            fecha_carga = form.cleaned_data['fecha_carga']
            imagenes = request.FILES.getlist('imagenes')

            nombres_de_archivos = []
            imagenes_a_crear = []
            for image in imagenes:
                nueva_imagen = Imagen(
                    imagen=image,
                    sitio=sitio,
                    fecha_carga=fecha_carga,
                    usuario=request.user
                )
                imagenes_a_crear.append(nueva_imagen)

            # Usar bulk_create para mejorar la eficiencia
            Imagen.objects.bulk_create(imagenes_a_crear)

            # Ahora iterar sobre las imágenes guardadas para obtener solo
            # los nombres finales
            for imagen in imagenes_a_crear:
                # Actualiza el objeto para obtener
                # datos como el nombre de archivo final
                imagen.refresh_from_db()
                result = convert_to_webp(imagen)
                messages.info(request, result)

            # Crear y guardar el comentario si existe alguno
            if comentario_texto:
                Comentario.objects.create(
                    sitio=sitio,
                    comentario=comentario_texto,
                    fecha_carga=fecha_carga,
                    usuario=request.user
                )

            # Añadir un mensaje de éxito
            messages.success(request, "Imágenes cargadas correctamente.")

            # Imprimir nombres de archivos para revisión
            print("Nombres de los archivos guardados:", nombres_de_archivos)

            return redirect('main:home_page')
        else:
            messages.error(
                request, "Se encontraron errores en el formulario,\
                    por favor corrígelos.")
            return render(request, "cargar.html", {'form': form})
    else:
        form = ImagesForm(user=request.user)
    return render(request, 'cargar.html', {'form': form})


def display_images_comments(request, site_id):
    # Obtener el sitio o mostrar un 404 si no existe
    sitio = get_object_or_404(Sitio, id=site_id)

    # Obtener fechas truncadas y ordenadas de imágenes y comentarios
    imagenes = Imagen.objects.filter(sitio=sitio).annotate(
        fecha_truncada=TruncMinute('fecha_carga')
        ).order_by('-fecha_truncada')

    comentarios = Comentario.objects.filter(sitio=sitio).annotate(
        fecha_truncada=TruncMinute('fecha_carga')
        ).order_by('-fecha_truncada')

    # Utilizar la fecha truncada directamente desde las consultas y
    # almacenarla en el formato correcto
    fechas_imagenes = set(imagenes.values_list('fecha_truncada', flat=True))
    fechas_comentarios = set(comentarios.values_list(
        'fecha_truncada', flat=True))

    # Unificar y ordenar las fechas
    fechas_unicas = sorted(fechas_imagenes | fechas_comentarios, reverse=True)

    items_por_fecha = OrderedDict(
        (fecha, {'imagenes': [], 'comentarios': []})
        for fecha in fechas_unicas)

    # Llenar el diccionario con imágenes
    for imagen in imagenes:
        # Aquí aseguramos que fecha_truncada ya es un objeto datetime
        fecha_key = imagen.fecha_truncada
        if fecha_key not in items_por_fecha:
            items_por_fecha[fecha_key] = {'imagenes': [], 'comentarios': []}
        items_por_fecha[fecha_key]['imagenes'].append(imagen)

    # Llenar el diccionario con comentarios
    for comentario in comentarios:
        # Similarmente, fecha_truncada debería ser un objeto datetime
        fecha_key = comentario.fecha_truncada
        if fecha_key not in items_por_fecha:
            items_por_fecha[fecha_key] = {'comentarios': []}
        user_profile = comentario.usuario.profile
        es_prevencionista = (user_profile.cargo == 'PRE'
                             if user_profile else False)
        comentario_info = {
            'comentario': comentario.comentario,
            'usuario': f"{comentario.usuario.first_name}\
                {comentario.usuario.last_name}",
            'es_prevencionista': es_prevencionista,
        }
        items_por_fecha[fecha_key]['comentarios'].append(comentario_info)

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
