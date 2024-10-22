from django.shortcuts import render
from actividades.models import DetalleProgreso, Progreso
from clientes.models import UserProfile
from galeria.models import Imagen, Comentario
from main.models import Contratista, Sitio
import json
from django.http import JsonResponse
# from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Max

MESES_ES = {
    1: 'enero',
    2: 'febrero',
    3: 'marzo',
    4: 'abril',
    5: 'mayo',
    6: 'junio',
    7: 'julio',
    8: 'agosto',
    9: 'septiembre',
    10: 'octubre',
    11: 'noviembre',
    12: 'diciembre',
}


def format_fecha(fecha):
    MESES_ES = {
        1: 'enero', 2: 'febrero', 3: 'marzo',
        4: 'abril', 5: 'mayo', 6: 'junio',
        7: 'julio', 8: 'agosto', 9: 'septiembre',
        10: 'octubre', 11: 'noviembre', 12: 'diciembre',
    }
    return f"{fecha.day} de {MESES_ES[fecha.month]} de {fecha.year}"


def sitio_data(sitio):
    return {
        'id': sitio.id,
        'sitio': sitio.sitio,
        'cod_id': sitio.cod_id,
        'nombre': sitio.nombre,
        'altura': sitio.altura,
        'lat': sitio.lat,
        'lon': sitio.lon,
        'contratista': sitio.contratista.name if sitio.contratista else None,
        'ito': f"{sitio.ito.user.first_name} {sitio.ito.user.last_name}"
        if sitio.ito else None,

    }


@login_required(login_url='login/')
def home(request):
    # Obtenemos el perfil del usuario autenticado
    user_profile = UserProfile.objects.get(user=request.user)

    # Utilizamos el manager para obtener los sitios
    sitios = Sitio.objects.for_user_profile(user_profile)

    # Filtrar los contratistas que están asociados con los sitios seleccionados
    contratistas = Contratista.objects.filter(sitio__in=sitios).distinct()

    sitios_data = []
    for sitio in sitios:
        # Obtenemos los datos del sitio
        sitio_data = {
            'id': sitio.id,
            'sitio': sitio.sitio,
            'cod_id': sitio.cod_id,
            'nombre': sitio.nombre,
            'altura': sitio.altura,
            'lat': sitio.lat,
            'lon': sitio.lon,
            'contratista': {
                'name': sitio.contratista.name,
                'cod': sitio.contratista.cod
            } if sitio.contratista else None,

            'ito': f"{sitio.ito.user.first_name} {sitio.ito.user.last_name}"
            if sitio.ito else None,

            'estado': sitio.estado
        }

        sitios_data.append(sitio_data)

    sitios_json = json.dumps(sitios_data)

    # Obtener una lista simple de códigos de contratistas
    contratistas_cod_list = list(contratistas.values_list('cod', flat=True))
    contratistas_json = json.dumps(contratistas_cod_list)

    context = {
        'sitios_json': sitios_json,
        'contratistas_json': contratistas_json
    }
    return render(request, 'home_page.html', context)


def get_site_data(request):
    site_id = request.GET.get('site_id')
    sitio = Sitio.objects.get(id=site_id)
    images = Imagen.objects.filter(sitio__id=site_id)
    comments = Comentario.objects.filter(sitio__id=site_id)
    progreso_gral = []

    try:
        progreso = Progreso.objects.get(progreso__proyecto__id=site_id)
        # Verificar si el progreso está activado
        if not progreso.activar:
            progreso_data = None
        else:
            detalles = DetalleProgreso.objects.filter(
                progreso=progreso, mostrar=True).select_related(
                    'actividad_grupo', 'actividad_grupo__actividad')
            progreso_data = [{
                'actividad': detalle.actividad_grupo.actividad.nombre,
                # 'grupo': detalle.actividad_grupo.grupo.nombre,
                'ponderacion': detalle.actividad_grupo.ponderacion,
                'avance': detalle.porcentaje,
            } for detalle in detalles]

            # Agregar información de fechas
            progreso_gral.append({
                'fecha_inicio': progreso.fecha_inicio.strftime('%Y-%m-%d')
                if progreso.fecha_inicio else '',

                'fecha_final': progreso.fecha_final.strftime('%Y-%m-%d')
                if progreso.fecha_final else ''
            })

    except Progreso.DoesNotExist:
        progreso_data = None

    latest_image_date = images.aggregate(
        Max('fecha_carga'))['fecha_carga__max']
    latest_date_images_str = latest_image_date.strftime('%d-%m-%Y')

    latest_comment_date = comments.aggregate(
        Max('fecha_carga'))['fecha_carga__max']
    latest_date_comment_str = format_fecha(latest_comment_date)

    images = images.filter(
        fecha_carga=latest_image_date
        ) if latest_image_date else Imagen.objects.none()
    comments = comments.filter(
        fecha_carga=latest_comment_date
        ) if latest_comment_date else Comentario.objects.none()

    image_data = [{
        'url': image.imagen.url,
        'description': image.descripcion or '',
        'fecha_carga': format_fecha(image.fecha_carga),
    } for image in images]

    comment_data = [{
        'comentario': comment.comentario or '',
        'fecha_carga': format_fecha(comment.fecha_carga),
        'usuario': f"{comment.usuario.first_name} {comment.usuario.last_name}"
        if comment.usuario else None,
    } for comment in comments]

    return JsonResponse({
        'images': image_data,
        'latest_date_images': latest_date_images_str,
        'comments': comment_data,
        'latest_date_comments': latest_date_comment_str,
        'sitio': sitio_data(sitio),
        'progreso': progreso_data,
        'progreso_gral': progreso_gral
    })


def get_full_site_data(request):
    pass
    # site_id = request.GET.get('site_id')
    # images = Imagen.objects.filter(
    #     sitio__id=site_id).order_by('fecha_carga')
    # comments = Comentario.objects.filter(
    #     sitio__id=site_id).order_by('fecha_carga')

    # # Agrupar imágenes y comentarios por fecha
    # data_por_fecha = defaultdict(lambda: {'imagenes': [], 'comentarios': []})

    # # Agregar datos específicos de imágenes y comentarios
    # for image in images:
    #     fecha = image.fecha_carga.date()
    #     data_por_fecha[fecha]['imagenes'].append({
    #         'url': image.imagen.url,
    #         'description': image.descripcion or '',
    #     })

    # for comment in comments:
    #     fecha = comment.fecha_carga.date()
    #     data_por_fecha[fecha]['comentarios'].append({
    #         'comentario': comment.comentario or '',
    #         'usuario': comment.usuario.username,
    #     })

    # # Función para formatear la fecha para
    # la presentación
    # def format_date(date):
    #     return f"{date.day} de {MESES_ES[date.month]} de {date.year}"

    # # Convertir el diccionario a una lista ordenada por fecha
    # data_ordenada = sorted(
    #     [{'fecha': format_date(
    # fecha), 'imagenes': data['imagenes'],
    # 'comentarios': data['comentarios']}
    #      for fecha, data in data_por_fecha.items()],
    #     key=lambda x: x['fecha']
    # )
    # return JsonResponse({'data': data_ordenada})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    # Redirige a los usuarios ya autenticados
    redirect_authenticated_user = True
    next_page = reverse_lazy('main:home_page')
