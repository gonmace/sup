# models.py
from django.conf import settings
from django.db import models
from streamfield.fields import StreamField
from galeria.models import Icon
from main.models import Sitio
from .middleware import RequestMiddleware
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


TEXT_BORDER_CHOICES = (
    ("rojo", "Rojo"),
    ("amarillo", "Amarillo"),
    ("verde", "Verde"),
    ("gris", "Gris"),
    ("azul", "Azul"),
)


class Text(models.Model):
    title = models.CharField("Titulo", max_length=100, blank=True, null=True)
    text = models.TextField("Texto", blank=True, null=True)
    border = models.CharField(
        "Color de borde",
        max_length=10,
        choices=TEXT_BORDER_CHOICES,
        blank=True,
        null=True
        )
    user_show = models.BooleanField("Firma de Usuario", default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="texts",
        blank=True,
        null=True,
        editable=False
    )
    date = models.DateField(default=timezone.now, editable=True)

    def save(self, *args, **kwargs):
        request = RequestMiddleware.get_request()
        if self._state.adding and request:
            self.user = request.user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | {self.text[:30]}"\
            if self.title else self.text[:30]

    class Meta:
        verbose_name = "Texto"
        verbose_name_plural = "Textos"


class ImageWithText(models.Model):
    image = models.ImageField(upload_to="folder/")
    text = models.TextField(null=True, blank=True)
    border = models.CharField(
        "Color de borde",
        max_length=10,
        choices=TEXT_BORDER_CHOICES,
        blank=True,
        null=True
        )
    date = models.DateField(default=timezone.now, editable=True)

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Imagen con Texto"
        verbose_name_plural = "Imagenes con Texto"
        


class OpenUrl(models.Model):
    url = models.URLField()
    text = models.CharField(max_length=100, blank=True, null=True)
    url2 = models.URLField(blank=True, null=True)
    text2 = models.CharField(max_length=100, blank=True, null=True)
    url3 = models.URLField(blank=True, null=True)
    text3 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.text} | {self.text2} | {self.text3}"

    verbose_name = "Enlace a Archivo"
    verbose_name_plural = "Enlaces a Archivos"

class MessageWithIcon(models.Model):
    icon = models.ForeignKey(
        Icon,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    message = models.CharField(max_length=100, blank=True, null=True)
    color_icon = models.CharField(
        "Color de Icono",
        max_length=10,
        choices=TEXT_BORDER_CHOICES,
        blank=True,
        null=True
        )
    date = models.DateField(default=timezone.now, editable=True)

    verbose_name = "Mensaje con Icono"
    verbose_name_plural = "Mensajes con Icono"

class RadialProgress(models.Model):
    title = models.CharField("Titulo", max_length=100, blank=True, null=True)
    progress = models.IntegerField("Porcentaje", default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    color = models.CharField(
        "Color",
        max_length=10,
        choices=TEXT_BORDER_CHOICES,
        blank=True,
        null=True
        )

    verbose_name = "Medidor de avance"
    verbose_name_plural = "Medidores de avance"

STREAMBLOCKS_MODELS = [
    Text,
    ImageWithText,
    OpenUrl,
    MessageWithIcon,
    RadialProgress,
]


class ProyectoComponentes(models.Model):
    sitio = models.ForeignKey(
        Sitio,
        on_delete=models.CASCADE,
        related_name="proyecto_componentes"
        )
    stream = StreamField(
        model_list=[
            Text,
            ImageWithText,
            OpenUrl,
            MessageWithIcon,
            RadialProgress,
        ],
        verbose_name="Componentes",
        )

    def __str__(self):
        return str(self.sitio)

    class Meta:
        verbose_name = "COMPONENTES"
        verbose_name_plural = "COMPONENTES"
