from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cod = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.cod


class Proyecto(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    cod = models.CharField(max_length=50)

    def __str__(self):
        return self.cod


CARGO = [
    ('SUP', 'Supervisor'),
    ('PRE', 'Prevencionista'),
    ('ADM', 'Administrador'),
    ('CLI', 'Cliente'),
    ('SEG', 'Seguimiento')
]


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cargo = models.CharField("Cargo", max_length=3, choices=CARGO)
    proyectos = models.ManyToManyField(Proyecto, verbose_name="Proyectos")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.user.username
