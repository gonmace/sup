from django.shortcuts import render
from galeria.models import Imagen, Comentario
from main.models import Contratista, Sitio, Avance
import json
from django.http import JsonResponse
from django.db.models import Max
from collections import defaultdict

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


def home(request):
    sitios = Sitio.objects.all()
    contratistas = Contratista.objects.all()
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
            'ito': sitio.ito.nombre if sitio.ito else None,
        }

        # Intentamos obtener el avance relacionado
        try:
            # Gracias al OneToOneField, podemos acceder directamente
            avance = sitio.avance
            avance_data = {
                'estado': avance.estado,
                'excavacion': avance.excavacion.strftime('%Y-%m-%d')
                if avance.excavacion else None,

                'hormigonado': avance.hormigonado.strftime('%Y-%m-%d')
                if avance.hormigonado else None,

                'montado': avance.montaje.strftime('%Y-%m-%d')
                if avance.montaje else None,

                'energia_prov': avance.ener_prov.strftime('%Y-%m-%d')
                if avance.ener_prov else None,

                'energia_def': avance.ener_def.strftime('%Y-%m-%d')
                if avance.ener_def else None,

                'porcentaje': avance.porcentaje,
                'fecha_fin': avance.fecha_fin.strftime('%Y-%m-%d')
                if avance.fecha_fin else None,

                'comentario': avance.comentario,
            }
        except Avance.DoesNotExist:
            # Si no existe un avance asociado
            avance_data = None

        # Agregamos el avance al sitio
        sitio_data['avance'] = avance_data

        sitios_data.append(sitio_data)

    sitios_json = json.dumps(sitios_data)

    # Obtener una lista simple de códigos de contratistas
    contratistas_cod_list = list(contratistas.values_list('cod', flat=True))
    contratistas_json = json.dumps(contratistas_cod_list)

    context = {
        'sitios_json': sitios_json,
        # Lista simple ["MER", "AJ", "GH3"]
        'contratistas_cod_list': contratistas_cod_list,
        # JSON ["MER", "AJ", "GH3"]
        'contratistas_json': contratistas_json
    }
    return render(request, 'home_page.html', context)


def get_site_images(request):
    site_id = request.GET.get('site_id')
    images = Imagen.objects.filter(sitio__id=site_id)
    sitio = Sitio.objects.get(id=site_id)
    comments = Comentario.objects.filter(sitio__id=site_id)

    # Obtener la fecha más reciente entre imágenes y comentarios
    latest_image_date = images.aggregate(
        Max('fecha_carga'))['fecha_carga__max']
    latest_comment_date = comments.aggregate(
        Max('fecha_carga'))['fecha_carga__max']

    # Manejar el caso en que ambas fechas sean None
    latest_dates = [date for date in
                    [latest_image_date, latest_comment_date]
                    if date is not None]
    latest_date = max(latest_dates) if latest_dates else None

    if latest_date:
        latest_date_str = f"""{latest_date.day} de
        {MESES_ES[latest_date.month]} de {latest_date.year}"""
    else:
        latest_date_str = ''

    # Filtrar imágenes y comentarios por la última fecha disponible
    if latest_date:
        images = images.filter(fecha_carga=latest_date)
        comments = comments.filter(fecha_carga=latest_date)
    else:
        images = Imagen.objects.none()
        comments = Comentario.objects.none()

    # Construir image_data
    image_data = []
    for image in images:
        fecha = image.fecha_carga
        fecha_formateada = f"""{fecha.day} de
        {MESES_ES[fecha.month]} de {fecha.year}"""
        image_data.append({
            'url': image.imagen.url,
            'description': image.descripcion or '',
            'fecha_carga': fecha_formateada,
        })

    # Obtener el último comentario
    latest_comment = comments.order_by('-fecha_carga').first()

    # Construir comment_data
    comment_data = []
    if latest_comment:
        fecha = latest_comment.fecha_carga
        fecha_formateada = f"""{fecha.day} de
        {MESES_ES[fecha.month]} de {fecha.year}"""
        comment_data.append({
            'comentario': latest_comment.comentario or '',
            'fecha_carga': fecha_formateada,
            'usuario': latest_comment.usuario.username,
        })

    return JsonResponse({
        'images': image_data,
        'latest_date': latest_date_str,
        'comments': comment_data,
        'sitio': {
            'sitio': sitio.sitio,
            'cod_id': sitio.cod_id,
            'nombre': sitio.nombre,
            'altura': sitio.altura,
            'contratista': sitio.contratista.name
            if sitio.contratista else None,
            'ito': sitio.ito.nombre if sitio.ito else None,
        }
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
