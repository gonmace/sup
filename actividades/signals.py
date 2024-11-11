from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    ActividadGrupo,
    ProyectoActividad,
    Progreso,
    DetalleProgreso
    )
from django.core.management import get_commands


def is_loading_fixtures():
    return 'loaddata' in get_commands()


@receiver(post_save, sender=ProyectoActividad)
def crear_progreso(sender, instance, created, **kwargs):
    if is_loading_fixtures():
        return
    if created:
        Progreso.objects.create(progreso=instance)


@receiver(post_save, sender=Progreso)
def crear_detalles_progreso(sender, instance, created, **kwargs):
    if is_loading_fixtures():
        return
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
