from django.db import models
from django.utils import timezone
from main.models import Sitio
from django.conf import settings
from .managers import ImagenManager, ComentarioManager
from PIL import Image


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Primero guardamos la imagen original
        self.convert_to_webp()  # Luego convertimos y guardamos la versión WebP

    def convert_to_webp(self):
        if self.imagen:
            original_path = self.imagen.path
            img = Image.open(original_path)
            webp_path = f"{original_path.rsplit('.', 1)[0]}.webp"
            img.save(webp_path, "WEBP", quality=40)

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


class Icon(models.Model):
    name = models.CharField("Nombre del Icono", max_length=20, unique=True)
    icon = models.TextField(
        "Icono",
        help_text="Codigo SVG https://icon-sets.iconify.design/"
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Icono"
        verbose_name_plural = "Iconos"
