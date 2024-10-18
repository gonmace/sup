from django.db import models
from django.utils import timezone
from main.models import Sitio
from django.conf import settings
from .managers import ImagenManager, ComentarioManager


class Imagen(models.Model):
    sitio = models.ForeignKey(
        Sitio,
        on_delete=models.CASCADE,
        related_name='imagenes'
        )
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.CharField(max_length=52, blank=True, null=True)
    fecha_carga = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='imagenes_subidas'
        )

    objects = ImagenManager()

    def __str__(self):
        return f"{self.sitio.sitio} - {self.fecha_carga}"

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"


class Comentario(models.Model):
    sitio = models.ForeignKey(
        Sitio,
        on_delete=models.CASCADE,
        related_name='comentarios'
        )
    comentario = models.TextField(blank=True, null=True)
    fecha_carga = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios_subidas'
        )

    objects = ComentarioManager()

    def __str__(self):
        comentario_truncado = (
            self.comentario[:75] + '...'
            if len(self.comentario) > 75
            else self.comentario
        )
        return f"{self.sitio.sitio} - {comentario_truncado}"
