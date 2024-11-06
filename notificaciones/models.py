from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class NotificacionPush(models.Model):
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuarios = models.ManyToManyField(
        User, related_name='notificaciones_push', blank=True)

    def __str__(self):
        return self.titulo


class SuscripcionNotificacion(models.Model):

    ALLOWED_MODELS = [
        'actividades.Progreso',
        'actividades.DetalleProgreso',
        'clientes.Cliente',
        'clientes.Proyecto',
        'clientes.UserProfile',
        'componentes.ProyectoComponentes',
        'galeria.Comentario',
        'main.Sitio',
        'main.Mensaje',
        'streamblocks.ProyectoComponentes',
    ]

    titulo = models.CharField(max_length=255,
                              blank=True,
                              null=True,
                              editable=False
                              )
    mensaje = models.TextField(
        "Mensaje",
        blank=True,
        null=True,
        help_text="Opcional - Se tiene un mensaje predefiniodo, \
            el mensaje ira despues al predefinido"
        )
    usuarios = models.ManyToManyField(
        User, related_name='suscripciones_notificaciones')
    modelo = models.OneToOneField(
        ContentType, on_delete=models.CASCADE, limit_choices_to={
            'model__in': [model.split('.')[1].lower()
                          for model in ALLOWED_MODELS],

            'app_label__in': [model.split('.')[0]
                              for model in ALLOWED_MODELS]}
        )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} para\
            {self.modelo.app_label}.{self.modelo.model}"
