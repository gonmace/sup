from django.db import models
from django.contrib.auth import get_user_model
from fcm_django.models import FCMDevice
from firebase_admin.messaging import (
    Message,
)

User = get_user_model()


class SendNotificacionPush(models.Model):
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuarios = models.ManyToManyField(
        FCMDevice, related_name='notificaciones_push')

    def __str__(self):
        return self.titulo

    def enviar_notificacion(self):
        devices = self.usuarios.all()
        if devices.exists():
            devices.send_message(Message(
                data={
                    'title': self.titulo,
                    'body': self.mensaje,
                    'icon': '/static/firebase-logo.png',
                    'actionUrl': 'https://google.com',
                }
            ))
        else:
            print("No hay dispositivos asociados para enviar la notificación.")
























# class SuscripcionNotificacion(models.Model):

#     ALLOWED_MODELS = [
#         'actividades.Progreso',
#         'actividades.DetalleProgreso',
#         'clientes.Cliente',
#         'clientes.Proyecto',
#         'clientes.UserProfile',
#         'componentes.ProyectoComponentes',
#         'galeria.Comentario',
#         'main.Sitio',
#         'main.Mensaje',
#         'streamblocks.ProyectoComponentes',
#     ]

#     titulo = models.CharField(max_length=255,
#                               blank=True,
#                               null=True,
#                               editable=False
#                               )
#     mensaje = models.TextField(
#         "Mensaje",
#         blank=True,
#         null=True,
#         help_text="Opcional - Se tiene un mensaje predefiniodo, \
#             el mensaje ira despues al predefinido"
#         )
#     usuarios = models.ManyToManyField(
#         User, related_name='suscripciones_notificaciones')
#     modelo = models.OneToOneField(
#         ContentType, on_delete=models.CASCADE, limit_choices_to={
#             'model__in': [model.split('.')[1].lower()
#                           for model in ALLOWED_MODELS],

#             'app_label__in': [model.split('.')[0]
#                               for model in ALLOWED_MODELS]}
#         )
#     fecha_creacion = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.titulo} para\
#             {self.modelo.app_label}.{self.modelo.model}"
