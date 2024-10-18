from django.db import models
from django.core.exceptions import ValidationError
from main.models import Sitio
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import ProgresoManager, DetalleProgresoManager


class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"


class GrupoActividades(models.Model):
    # Nombre único para cada grupo (por ejemplo, 'default')
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Grupo de Actividades"
        verbose_name_plural = "Grupos de Actividades"


class ActividadGrupo(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoActividades, on_delete=models.CASCADE)
    ponderacion = models.FloatField()

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        unique_together = ('actividad', 'grupo')
        ordering = ['order']

    def clean(self):
        super().clean()
        if self.ponderacion is None:
            raise ValidationError(
                f"Debes asignar un número para la actividad \
                    '{self.actividad.nombre}' en el grupo \
                        '{self.grupo.nombre}'.")

    def save(self, *args, **kwargs):
        # Si el campo 'order' no está establecido
        # (es decir, es 0 o no se ha modificado)
        if not self.order:
            # Obtener el valor máximo de 'order' para el grupo específico
            max_order = ActividadGrupo.objects.filter(
                grupo=self.grupo).aggregate(
                    max_order=models.Max('order'))['max_order']
            # Asignar el siguiente valor disponible
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.actividad.nombre}"


class ProyectoActividad(models.Model):
    proyecto = models.OneToOneField(Sitio, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoActividades, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proyecto con Actividades"
        verbose_name_plural = "Proyectos con Actividades"

    def __str__(self):
        return f"{self.proyecto} ---> {self.grupo}"


@receiver(post_save, sender=ProyectoActividad)
def crear_progreso(sender, instance, created, **kwargs):
    if created:
        Progreso.objects.create(progreso=instance)


class Progreso(models.Model):
    progreso = models.OneToOneField(
        ProyectoActividad, on_delete=models.CASCADE)
    activar = models.BooleanField(default=True)
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_final = models.DateField(blank=True, null=True)

    objects = ProgresoManager()

    def __str__(self):
        return f"{self.progreso.proyecto}"


@receiver(post_save, sender=Progreso)
def crear_detalles_progreso(sender, instance, created, **kwargs):
    if created:
        actividades = ActividadGrupo.objects.filter(
            grupo=instance.progreso.grupo).order_by('order')
        for actividad in actividades:
            DetalleProgreso.objects.create(
                progreso=instance,
                actividad_grupo=actividad,
                porcentaje=0,
                order=actividad.order
                )


class DetalleProgreso(models.Model):
    progreso = models.ForeignKey(
        Progreso, on_delete=models.CASCADE, related_name='detalles')
    actividad_grupo = models.ForeignKey(
        ActividadGrupo, on_delete=models.CASCADE)
    porcentaje = models.FloatField("Avance %", default=0.0)
    mostrar = models.BooleanField("Agregar", default=True)
    order = models.PositiveIntegerField(default=0)

    objects = DetalleProgresoManager()

    def __str__(self):
        return f"Grupo {self.actividad_grupo.grupo} \
            | Ponderación: {self.actividad_grupo.ponderacion} \
                | Completado: {self.porcentaje}% "

    class Meta:
        verbose_name = "Detalle de Progreso"
        verbose_name_plural = "Detalles de Progresos"
        ordering = ['order']
