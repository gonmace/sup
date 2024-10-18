from django.shortcuts import render
from actividades.models import DetalleProgreso, Progreso
from clientes.models import UserProfile
from galeria.models import Imagen, Comentario
from main.models import Contratista, Sitio
import json
from django.http import JsonResponse
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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

    # Utilizamos el manager para obtener los contratistas
    contratistas = Contratista.objects.for_sitios(sitios)

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
    images = Imagen.objects.latest_for_sitio(site_id)
    comments = Comentario.objects.latest_for_sitio(site_id)

    progreso = Progreso.objects.get_active_for_sitio(site_id)
    progreso_data = None
    progreso_gral = []

    if progreso:
        detalles = DetalleProgreso.objects.for_progreso(progreso)
        progreso_data = [{
            'actividad': detalle.actividad_grupo.actividad.nombre,
            'ponderacion': detalle.actividad_grupo.ponderacion,
            'avance': detalle.porcentaje,
        } for detalle in detalles]

        progreso_gral.append({
            'fecha_inicio': (
                progreso.fecha_inicio.strftime('%Y-%m-%d')
                if progreso.fecha_inicio else ''
                ),
            'fecha_final': (
                progreso.fecha_final.strftime('%Y-%m-%d')
                if progreso.fecha_final else ''
                )
        })

    images_data = [{
        'url': image.imagen.url,
        'description': image.descripcion or '',
        'fecha_carga': image.fecha_carga,
    } for image in images]

    comments_data = [{
        'comentario': comment.comentario or '',
        'fecha_carga': comment.fecha_carga,
        'usuario': (
            f"{comment.usuario.first_name} {comment.usuario.last_name}"
            if comment.usuario else None
            ),
    } for comment in comments]

    return JsonResponse({
        'images': images_data,
        'comments': comments_data,
        'sitio': sitio_data(sitio),
        'progreso': progreso_data,
        'progreso_gral': progreso_gral
    })


def get_full_site_data(request):
    site_id = request.GET.get('site_id')
    images = Imagen.objects.filter(sitio__id=site_id).order_by('fecha_carga')
    comments = Comentario.objects.filter(
        sitio__id=site_id).order_by('fecha_carga')

    # Agrupar imágenes y comentarios por fecha
    data_por_fecha = defaultdict(lambda: {'imagenes': [], 'comentarios': []})

    for image in images:
        fecha = image.fecha_carga.date()
        fecha_formateada = f"""{fecha.day} de
        {MESES_ES[fecha.month]} de {fecha.year}"""
        data_por_fecha[fecha_formateada]['imagenes'].append({
            'url': image.imagen.url,
            'description': image.descripcion or '',
            'fecha_carga': fecha_formateada,
        })

    for comment in comments:
        fecha = comment.fecha_carga.date()
        fecha_formateada = f"""{fecha.day} de
        {MESES_ES[fecha.month]} de {fecha.year}"""
        data_por_fecha[fecha_formateada]['comentarios'].append({
            'comentario': comment.comentario or '',
            'fecha_carga': fecha_formateada,
            'usuario': comment.usuario.username,
        })

    # Convertir el diccionario a una lista ordenada por fecha
    data_ordenada = []
    for fecha in sorted(data_por_fecha.keys()):
        data_ordenada.append({
            'fecha': fecha,
            'imagenes': data_por_fecha[fecha]['imagenes'],
            'comentarios': data_por_fecha[fecha]['comentarios'],
        })

    return JsonResponse({
        'data': data_ordenada,
    })


class CustomLoginView(LoginView):
    template_name = 'login.html'
    # Redirige a los usuarios ya autenticados
    redirect_authenticated_user = True
    next_page = reverse_lazy('main:home_page')
