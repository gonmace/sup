from django.shortcuts import get_object_or_404, render, redirect

from main.models import Sitio
from .forms import ImagesForm
from .models import Imagen, Comentario
from django.contrib import messages
from django.db.models import DateField
from django.db.models.functions import Trunc
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


@login_required(login_url='login/')
def fileupload(request):
    if request.method == 'POST':
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
            return redirect('main:home_page')  # Redirigir a la página de éxito
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
    # Obtener fechas truncadas y ordenadas de imágenes y comentarios
    imagenes = Imagen.objects.filter(sitio=sitio).annotate(
        fecha=Trunc('fecha_carga', 'day', output_field=DateField())
    ).order_by('-fecha')

    comentarios = Comentario.objects.filter(sitio=sitio).annotate(
        fecha=Trunc('fecha_carga', 'day', output_field=DateField())
    ).order_by('-fecha')

    # Obtener todas las fechas únicas de imágenes y comentarios
    fechas_imagenes = imagenes.values_list('fecha', flat=True).distinct()
    fechas_comentarios = comentarios.values_list('fecha', flat=True).distinct()

    # Unificar y ordenar fechas
    fechas_unicas = sorted(
        set(fechas_imagenes) | set(fechas_comentarios), reverse=True
        )

    items_por_fecha = OrderedDict(
        (
            fecha,
            {'imagenes': [], 'comentarios': []}) for fecha in fechas_unicas
        )

    # Llenar el diccionario con imágenes y comentarios
    for imagen in imagenes:
        items_por_fecha[imagen.fecha]['imagenes'].append(imagen)

    for comentario in comentarios:
        user_profile = comentario.usuario.userprofile_set.first()
        es_prevencionista = (
            user_profile.cargo == 'PRE' if user_profile else False
            )
        comentario_info = {
            'comentario': comentario.comentario,
            'usuario': f"{comentario.usuario.first_name}\
                {comentario.usuario.last_name}",
            'fecha': comentario.fecha,
            'es_prevencionista': es_prevencionista,
        }
        items_por_fecha[comentario.fecha]['comentarios'].append(
            comentario_info
            )

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
