from django.db import models
from clientes.models import Proyecto, UserProfile
from .managers import SitioManager, ContratistaManager

ESTADO_CHOICES = [
    ('ASG', 'Asignado',),
    ('EJE', 'Ejecución'),
    ('TER', 'Terminado'),
    ('PTG', 'Postergado'),
    ('CAN', 'Cancelado'),
]


class Contratista(models.Model):
    name = models.CharField("Contratista", max_length=20)
    cod = models.CharField("Codigo", max_length=3, help_text="3 Caracteres")
    
    objects = ContratistaManager()

    def __str__(self):
        return f"{self.cod}"


class Sitio(models.Model):
    sitio = models.CharField("Codigo Sitio", max_length=10,  null=True)
    cod_id = models.CharField("Codigo Cliente", max_length=10)
    nombre = models.CharField(max_length=100, blank=True)
    altura = models.IntegerField("Altura", blank=True, null=True)
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
        return f"{self.sitio}"


# class Avance(models.Model):
#     sitio = models.OneToOneField(Sitio, on_delete=models.CASCADE)
#     estado = models.CharField(
#         "Estado",
#         max_length=3,
#         choices=ESTADO_CHOICES,
#         default='EJE'
#         )
#     excavacion = models.DateField("Excavación", null=True, blank=True)
#     hormigonado = models.DateField("Hormigonado", null=True, blank=True)
#     montaje = models.DateField("Montaje", null=True, blank=True)
#     ener_prov = models.DateField(
    # "Energía Provisional", null=True, blank=True)
#     ener_def = models.DateField("Energía Definitiva", null=True, blank=True)
#     porcentaje = models.FloatField("Porcentaje", default=0.0)
#     fecha_fin = models.DateField("Fecha Fin", blank=True, null=True)
#     comentario = models.TextField("Comentarios", blank=True, null=True)

#     class Meta:
#         verbose_name = "Avance"
#         verbose_name_plural = "Avance Proyectos"

#     def __str__(self):
#         return f"{self.sitio}"
