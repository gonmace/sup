# notificationes/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from actividades.models import DetalleProgreso
from clientes.models import UserProfile
from galeria.models import Comentario
from .models import SendNotificacionPush
from django.db.models.signals import m2m_changed
from firebase_admin.messaging import Message
from .middleware import UserMiddleware


# Reduce el comentario a 100 caracteres
def truncate_comment(comentario):
    # Verificar si el comentario excede los 100 caracteres
    if len(comentario) > 100:
        # Cortar el comentario a 100 caracteres y añadir puntos suspensivos
        return comentario[:100] + '...'
    else:
        # Devolver el comentario original si no excede los 100 caracteres
        return comentario


# tipòs es cliente o daministrador del modelo clientes
def get_usuarios_from_proyecto(proyecto, tipo):
    # Filtrar todos los UserProfile que tienen este proyecto en
    # su campo ManyToMany 'proyectos'
    user_profiles = UserProfile.objects.filter(
        proyectos=proyecto, tipo_notificacion=tipo)

    # Devolver la lista de usuarios relacionados a esos perfiles
    usuarios = [profile.user for profile in user_profiles]
    return usuarios


# @receiver(post_save, sender=FCMDevice)
# def crear_notificacion_usuario(sender, instance, created, **kwargs):
#     """Crea el tipo de niotificacion que debe generarse por cada usuario
#     al registrar un dispositivo.
#     Si el dispositivo fue creado (no actualizado)"""
#     if created:
#         # Crear un registro en UsuarioNotificacion asociado al
# nuevo FCMDevice
#         UsuarioNotificacion.objects.create(usuario=instance)


@receiver(post_save, sender=SendNotificacionPush)
def enviar_notificacion_post_save(sender, instance, created, **kwargs):
    """ Envia la notificación al usuario si los dispositivos existen
        y se ha modificado o guardado un SendNotificacionPush,
        de lo contrario no hace nada. OJO que los dispositivos
        unicamente se registran despues de haberse guadado el registro,
        por lo que no se puede enviar la notificación sin antes haberlo
        guardado"""
    devices = instance.usuarios.all()
    if devices.exists():
        instance.enviar_notificacion()


@receiver(m2m_changed, sender=SendNotificacionPush.usuarios.through)
def enviar_notificacion_usuarios(sender, instance, action, **kwargs):
    """ Envia la notificación al usuario si los dispositivos existen
        y el registro SendNotificacionPush es nuevo
        de lo contrario no hace nada. """
    if action == 'post_add':
        instance.enviar_notificacion()


# NOTIFICACION DE AVANCE (actividades)
@receiver(post_save, sender=DetalleProgreso)
def enviar_notificacion_avance(sender, instance, created, **kwargs):
    if not created:
        usuario_modifico = UserMiddleware.get_current_user()

        # detectar a que proyecto corresponde
        proyecto = instance.progreso.progreso.proyecto.proyecto

        # detectar a que sitio corresponde
        sitio = instance.progreso.progreso.proyecto
        sitio_id = sitio.id
        # filtrar los usuarios clientes que estan en ese proyecto
        # 1 es cliente
        usuarios_cliente = get_usuarios_from_proyecto(proyecto, 1)

        # filtrar los usuarios administradores que estan en ese proyecto
        # 2 es administrador
        usuarios_administrador = get_usuarios_from_proyecto(proyecto, 2)

        # devices clientes y luego adminitradores
        devices_cliente = FCMDevice.objects.filter(
            user__in=usuarios_cliente
            )
        devices_administrador = FCMDevice.objects.filter(
            user__in=usuarios_administrador
            )

        if devices_cliente.exists():
            devices_cliente.send_message(Message(
                data={
                    'title': str(sitio),
                    'body': "Progreso actualizado",
                    'icon': f"{settings.SITE_URL}/static/firebase-logo.png",
                    'actionUrl': f"{settings.SITE_URL}/?sitio_numero={sitio_id}",
                }
            ))

        if devices_administrador.exists():
            devices_administrador.send_message(Message(
                data={
                    'title': str(sitio),
                    'body': f"Progreso actualizado por {usuario_modifico}",
                    'icon': f"{settings.SITE_URL}/static/firebase-logo.png",
                    'actionUrl': f"{settings.SITE_URL}/?sitio_numero={sitio_id}",
                }
            ))


@receiver(post_save, sender=Comentario)
def enviar_notificacion_reporte(sender, instance, created, **kwargs):
    usuario_modifico = UserMiddleware.get_current_user()

    # detectar a que proyecto corresponde
    proyecto = instance.sitio.proyecto

    # detectar a que sitio corresponde
    sitio = instance.sitio
    sitio_id = sitio.id

    # filtrar los usuarios clientes que estan en ese proyecto
    # 1 es cliente
    usuarios_cliente = get_usuarios_from_proyecto(proyecto, 1)

    # filtrar los usuarios administradores que estan en ese proyecto
    # 2 es administrador
    usuarios_administrador = get_usuarios_from_proyecto(proyecto, 2)

    comentario = truncate_comment(instance.comentario)

    # devices clientes y luego adminitradores
    devices_cliente = FCMDevice.objects.filter(
        user__in=usuarios_cliente
        )
    devices_administrador = FCMDevice.objects.filter(
        user__in=usuarios_administrador
        )

    if devices_cliente.exists():
        devices_cliente.send_message(Message(
            data={
                'title': str(sitio),
                'body': comentario,
                'icon': f"{settings.SITE_URL}/static/firebase-logo.png",
                'actionUrl': f"{settings.SITE_URL}/imgs/{sitio_id}/",
            }
        ))

    if devices_administrador.exists():
        devices_administrador.send_message(Message(
            data={
                'title': str(sitio),
                'body': f"{comentario} - {usuario_modifico}",
                'icon': f"{settings.SITE_URL}/static/firebase-logo.png",
                'actionUrl': f"{settings.SITE_URL}/imgs/{sitio_id}/",
            }
        ))
