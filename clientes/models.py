from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class LogoRedLine(models.Model):
    name = models.CharField(max_length=20)
    logo = models.FileField(
        "Logo",
        upload_to='logos',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'svg'])],
        help_text="Formato PNG o SVG"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logos"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cod = models.CharField(max_length=3, unique=True)
    logo_mostrar = models.ForeignKey(
        LogoRedLine,
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )

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
    ('SEG', 'Seguimiento'),
    ('CTT', 'Contratista'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    cargo = models.CharField("Cargo", max_length=3, choices=CARGO)
    proyectos = models.ManyToManyField(Proyecto, verbose_name="Proyectos")
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='user_profile',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.user.username
