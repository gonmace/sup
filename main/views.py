from django.shortcuts import render
from actividades.models import DetalleProgreso, Progreso
from clientes.models import UserProfile
from galeria.models import Imagen, Comentario
from main.models import Chat, Contratista, Mensaje, Sitio
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Max
from .forms import MensajeForm
from django.utils.timezone import localtime
import json


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
    user_profile = UserProfile.objects.get(user=request.user)
    user_id = request.user.id
    sitios = Sitio.objects.for_user_profile(user_profile)
    contratistas = Contratista.objects.filter(sitio__in=sitios).distinct()

    form = MensajeForm()  # Inicializar el formulario para solicitudes GET

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            sitio_id = form.cleaned_data['sitio_id']
            sitio = Sitio.objects.get(pk=sitio_id)
            chat, created = Chat.objects.get_or_create(sitio=sitio)

            mensaje = form.save(commit=False)
            mensaje.chat = chat
            mensaje.usuario = request.user.profile
            mensaje.save()

            # dentro de tu vista, en la parte que maneja
            # la solicitud POST y AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response_data = {
                    'message': 'Mensaje enviado con éxito',
                    'data': {
                        'mensaje_id': mensaje.id,
                        'texto': mensaje.mensaje,
                        'usuario_id': request.user.id,
                        'usuario_nombre': request.user.get_full_name(),
                        'timestamp': localtime().strftime('%d-%m-%Y %H:%M')
                    }
                }
                return JsonResponse(response_data, status=200)

    context = {
        'user_id': user_id,
        'form': form,
        'sitios_json': json.dumps([{
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
        } for sitio in sitios]),
        'contratistas_json': json.dumps(
            list(contratistas.values_list('cod', flat=True)))
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
    latest_date_images_str = latest_image_date.strftime('%d-%m-%Y')\
        if latest_image_date else ''

    latest_comment_date = comments.aggregate(
        Max('fecha_carga'))['fecha_carga__max']
    latest_date_comment_str = format_fecha(latest_comment_date)\
        if latest_comment_date else ''

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


class CustomLoginView(LoginView):
    template_name = 'login.html'
    # Redirige a los usuarios ya autenticados
    redirect_authenticated_user = True
    next_page = reverse_lazy('main:home_page')


def get_chats(request, site_id, cant):
    # Obteniendo los mensajes y ordenándolos por fecha y hora
    if cant == 0:
        # Si cant es 0, obtenemos todos los mensajes sin limitar la cantidad
        mensajes = Mensaje.objects.filter(
            chat__sitio_id=site_id).order_by('-datetime')
    else:
        # Si cant es un número positivo,
        # limitamos la consulta a ese número de mensajes
        mensajes = Mensaje.objects.filter(
            chat__sitio_id=site_id).order_by('-datetime')[:cant]

    # Preparando la lista de mensajes con la información del usuario
    mensajes_data = [
        {
            "id": mensaje.id,
            "chat_id": mensaje.chat.id,
            "mensaje": mensaje.mensaje,
            "datetime": mensaje.datetime.strftime("%d-%m-%Y %H:%M"),

            "usuario_id": mensaje.usuario.user.id
            if mensaje.usuario and mensaje.usuario.user else None,

            "usuario_nombre": mensaje.usuario.user.get_full_name()
            if mensaje.usuario and mensaje.usuario.user else "Anónimo"
        }
        for mensaje in mensajes
    ]

    # Serializando la lista a JSON
    data = json.dumps(mensajes_data)
    return HttpResponse(data, content_type="application/json")


def delete_chat(request, chat_id, item_id):
    chat = Chat.objects.get(id=chat_id)
    item = chat.mensajes.get(id=item_id)
    item.delete()
    return JsonResponse({"message": "Chat eliminado con exito..."})
