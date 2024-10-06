from django.db import models


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
    name = models.CharField("Nombre", max_length=25)
    cargo = models.CharField("Cargo", max_length=3, choices=CARGO)

    def __str__(self):
        return f"{self.name}"

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
