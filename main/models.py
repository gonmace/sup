from django.db import models
from django.contrib.auth.models import User


class Contratista(models.Model):
    name = models.CharField("Contratista", max_length=20)
    cod = models.CharField("Codigo", max_length=3, help_text="3 Caracteres")

    def __str__(self):
        return f"{self.cod}"


CARGO = [
    ('SUP', 'Supervisor'),
    ('PRE', 'Prevencionista')
]


class Supervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cargo = models.CharField("Cargo", max_length=3, choices=CARGO)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"


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
        Supervisor,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return f"{self.sitio}"


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
    excavacion = models.DateField("Excavación", null=True, blank=True)
    hormigonado = models.DateField("Hormigonado", null=True, blank=True)
    montaje = models.DateField("Montaje", null=True, blank=True)
    ener_prov = models.DateField("Energía Provisional", null=True, blank=True)
    ener_def = models.DateField("Energía Definitiva", null=True, blank=True)
    porcentaje = models.FloatField("Porcentaje", default=0.0)
    fecha_fin = models.DateField("Fecha Fin", blank=True, null=True)
    comentario = models.TextField("Comentarios", blank=True, null=True)

    class Meta:
        verbose_name = "Avance"
        verbose_name_plural = "Avance Proyectos"

    def __str__(self):
        return f"{self.sitio}"
