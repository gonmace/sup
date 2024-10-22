from django.db import models


class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo


class Bloque(models.Model):
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='bloques'
        )
    nombre = models.CharField(max_length=200)
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Utilice los controles de arrastrar y soltar para reordenar.'
        )

    class Meta:
        ordering = ['orden']
        verbose_name = 'Bloque de Contenido'
        verbose_name_plural = 'Bloques de Contenido'

    def __str__(self):
        return str(self.nombre)


class Card(models.Model):
    bloque = models.ForeignKey(
        Bloque,
        on_delete=models.CASCADE,
        related_name='cards'
        )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=0)
    # Otros campos específicos de Tarjeta

    def __str__(self):
        return self.titulo


class Imagen(models.Model):
    bloque = models.ForeignKey(
        Bloque,
        on_delete=models.CASCADE,
        related_name='imgs'
        )
    archivo_imagen = models.ImageField(upload_to='imagenes/')
    orden = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nombre
