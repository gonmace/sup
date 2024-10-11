from django.db import models
from django.core.exceptions import ValidationError
from main.models import Sitio

from django.db.models.signals import post_save
from django.dispatch import receiver


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

    class Meta:
        unique_together = ('actividad', 'grupo')

    def clean(self):
        super().clean()
        if self.ponderacion is None:
            raise ValidationError(
                f"Debes asignar un número para la actividad \
                    '{self.actividad.nombre}' en el grupo \
                        '{self.grupo.nombre}'.")

    def __str__(self):
        return f"{self.actividad.nombre}"


class ProyectoActividad(models.Model):
    proyecto = models.OneToOneField(Sitio, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoActividades, on_delete=models.CASCADE)

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

    def __str__(self):
        return f"{self.progreso.proyecto}"


@receiver(post_save, sender=Progreso)
def crear_detalles_progreso(sender, instance, created, **kwargs):
    if created:
        actividades = ActividadGrupo.objects.filter(
            grupo=instance.progreso.grupo)
        for actividad in actividades:
            DetalleProgreso.objects.create(
                progreso=instance, actividad_grupo=actividad, porcentaje=0)


class DetalleProgreso(models.Model):
    progreso = models.ForeignKey(
        Progreso, on_delete=models.CASCADE, related_name='detalles')
    actividad_grupo = models.ForeignKey(
        ActividadGrupo, on_delete=models.CASCADE)
    porcentaje = models.FloatField("Avance %", default=0.0)
    mostrar = models.BooleanField(default=True)

    def __str__(self):
        return f"Grupo {self.actividad_grupo.grupo} \
            | Ponderación: {self.actividad_grupo.ponderacion} \
                | Completado: {self.porcentaje}% "

    class Meta:
        verbose_name = "Detalle de Progreso"
        verbose_name_plural = "Detalles de Progresos"
