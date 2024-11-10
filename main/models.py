from django.db import models
from clientes.models import Proyecto, UserProfile
from .managers import SitioManager, ContratistaManager


class Operador(models.Model):
    name = models.CharField("Operador", max_length=20)

    def __str__(self):
        return f"{self.name}"


class Contratista(models.Model):
    name = models.CharField("Contratista", max_length=20)
    cod = models.CharField("Codigo", max_length=3, help_text="3 Caracteres")

    objects = ContratistaManager()

    def __str__(self):
        return f"{self.cod}"


ESTADO_CHOICES = [
    ('ASG', 'Asignado',),
    ('EJE', 'Ejecución'),
    ('TER', 'Terminado'),
    ('PTG', 'Postergado'),
    ('CAN', 'Cancelado'),
]


class Sitio(models.Model):
    sitio = models.CharField("Codigo Sitio", max_length=12,  null=True)
    cod_id = models.CharField(
        "Codigo Cliente", max_length=10, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True)
    altura = models.IntegerField("Altura", blank=True, null=True)
    operador = models.ForeignKey(
        Operador,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    contratista = models.ForeignKey(
        Contratista,
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    lat = models.FloatField("Latitud", max_length=11)
    lon = models.FloatField("Longitud", max_length=11)
    ito = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'cargo': 'SUP'},
    )
    estado = models.CharField(
        "Estado",
        max_length=3,
        choices=ESTADO_CHOICES,
        blank=True,
        null=True
        )
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    objects = SitioManager()

    def __str__(self):
        return f"{self.sitio} | {self.nombre}"

    class Meta:
        ordering = ['sitio']


class Chat(models.Model):
    sitio = models.OneToOneField(
        Sitio, on_delete=models.CASCADE, related_name='chat'
        )
    activar = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sitio}"


class Mensaje(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='mensajes')
    usuario = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='mensajes')
    mensaje = models.CharField("Mensaje", max_length=500)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.user.username}: {self.mensaje[:40]}"
