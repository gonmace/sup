# notificationes/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from .models import SendNotificacionPush, UsuarioNotificacion
from django.db.models.signals import m2m_changed


@receiver(post_save, sender=FCMDevice)
def crear_notificacion_usuario(sender, instance, created, **kwargs):
    """Crea el tipo de niotificacion que debe generarse por cada usuario
    al registrar un dispositivo.
    Si el dispositivo fue creado (no actualizado)"""
    if created:
        # Crear un registro en UsuarioNotificacion asociado al nuevo FCMDevice
        UsuarioNotificacion.objects.create(usuario=instance)


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

# # notificaciones/signals.py
# from django.conf import settings
# from django.dispatch import receiver
# from fcm_django.models import FCMDevice
# from django.contrib.auth import get_user_model
# from firebase_admin.messaging import Message, Notification, AndroidConfig, AndroidNotification, WebpushNotification
# from django.db.models.signals import m2m_changed, post_save
# from actividades.models import Progreso
# from notificaciones.middleware import get_current_user
# from .models import NotificacionPush
# import logging
# from .models import SuscripcionNotificacion
# from django.templatetags.static import static

# User = get_user_model()
# logger = logging.getLogger(__name__)


# # ENVIAR  UNA NOTIFICACION PERSONALIZADA
# @receiver(post_save, sender=NotificacionPush)
# def enviar_notificacion_push_al_guardar(sender, instance, created, **kwargs):
#     # URL de la imagen para la notificación
#     # image_url = f"{settings.STATIC_URL}firebase-logo.png"
#     image_url = 'https://dcfb-189-28-76-62.ngrok-free.app/firebase-logo.png'
#     # Enviar notificación solo cuando el registro es nuevo o se ha modificado
#     for usuario in instance.usuarios.all():
#         dispositivos = FCMDevice.objects.filter(user=usuario)
#         if dispositivos.exists():
#             try:
#                 # Crear el mensaje de notificación
#                 message = Message(
#                     notification=WebpushNotification(
#                         title=instance.titulo,
#                         body=instance.mensaje,
#                         # image=image_url
#                     ),
#                     # android=AndroidConfig(
#                     #     priority='normal',
#                     #     notification=AndroidNotification(
#                     #         title=instance.titulo,
#                     #         body=instance.mensaje,
#                     #     )
#                     # )
#                     # android=AndroidConfig(
#                     #     priority='high',
#                     #     notification=AndroidNotification(
#                     #         title=instance.titulo,
#                     #         body=instance.mensaje,
#                     #         icon=image_url,  # Assuming this is the small icon
#                     #         image=image_url  # This is for the larger image in the notification
#                     #     )
#                     # )
#                 )
#                 # Enviar la notificación a los dispositivos del usuario
#                 dispositivos.send_message(message=message)

#             except Exception as e:
#                 logger.error(
#                     f"Error al enviar notificación al usuario {usuario.username}: {e}"
#                 )


# # @receiver(post_save, sender=Progreso)
# # def enviar_notificacion_progreso(request, sender, instance, created, **kwargs):
# #     # Configuración del mensaje específico para `Comentario`
# #     titulo = f"{instance.progreso.proyecto}"

# #     # URL del icono personalizado
# #     icon_url = f"{settings.SITE_URL}{static('img/logo_tekon.png')}"

# #     usuario_modificador = get_current_user()

# #     # Obtener la suscripción correspondiente al modelo Progreso
# #     suscripciones = SuscripcionNotificacion.objects.filter(
# #         modelo__model='progreso')

# #     for suscripcion in suscripciones:
# #         # Selecciona el mensaje de la suscripción y
# #         # adapta según el tipo de evento
# #         mensaje_evento = ("Nuevo proyecto registrado para Progreso."
# #                           if created else "Progreso actualizado.")
# #         mensaje_personalizado = f"{mensaje_evento} {suscripcion.mensaje}"\
# #             if suscripcion.mensaje else mensaje_evento

# #         # Personalizar el mensaje con el usuario que hizo la modificación
# #         if usuario_modificador:
# #             # Obtiene la primera letra de `first_name`,
# #             # la convierte a mayúscula, y le añade un punto
# #             inicial_nombre = (
# #                 usuario_modificador.first_name[0].capitalize() + "."
# #                 )

# #             if created:
# #                 mensaje = (f"{mensaje_personalizado} - Creado por: \
# # {inicial_nombre}{usuario_modificador.last_name}")
# #             else:
# #                 mensaje = (f"{mensaje_personalizado} - Modificado por: \
# # {inicial_nombre}{usuario_modificador.last_name}")
# #         else:
# #             mensaje = mensaje_personalizado

# #         # Enviar notificación a cada usuario en la suscripción
# #         for usuario in suscripcion.usuarios.all():
# #             dispositivos = FCMDevice.objects.filter(user=usuario, type='web')
# #             if dispositivos.exists():
# #                 try:
# #                     # Crea y envía el mensaje de notificación
# #                     message = Message(
# #                         notification=Notification(
# #                             title=titulo,
# #                             body=mensaje,
# #                             icon=icon_url
# #                         )
# #                     )
# #                     dispositivos.send_message(message=message)
# #                 except Exception as e:
# #                     print(f"Error al enviar notificación al usuario \
# # {usuario.username}: {e}")
