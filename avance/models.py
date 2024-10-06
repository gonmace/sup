from django.db import models
from main.models import Sitio

ESTADO_CHOICES = [
    ('ASG', 'Asignado',),
    ('EJE', 'Ejecución'),
    ('TER', 'Terminado'),
    ('PTG', 'Postergado'),
    ('CAN', 'Cancelado'),
]


class Avance(models.Model):
    sitio = models.OneToOneField(Sitio, on_delete=models.CASCADE)
    estado = models.CharField(
        "Estado",
        max_length=3,
        choices=ESTADO_CHOICES,
        default='EJE'
        )
    excavacion = models.DateField("Exc.", null=True, blank=True)
    hormigonado = models.DateField("Hor.", null=True, blank=True)
    montado = models.DateField("Mon.", null=True, blank=True)
    empalmeE = models.DateField("Ele.", null=True, blank=True)
    porcentaje = models.FloatField("Porcentaje", default=0.0)
    fechaFin = models.DateField("Fecha Fin", blank=True, null=True)
    comentario = models.TextField("Comentarios", blank=True, null=True)

    class Meta:
        verbose_name = "Avance"
        verbose_name_plural = "Avance Proyectos"

    def __str__(self):
        return f"{self.sitio}"
