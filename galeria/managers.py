from django.db import models


class ImagenManager(models.Manager):
    def for_sitio(self, sitio_id):
        # Filtra las imágenes de un sitio específico
        return self.filter(sitio__id=sitio_id).order_by('fecha_carga')

    def latest_for_sitio(self, sitio_id):
        # Obtiene las imágenes más recientes para un sitio específico
        latest_date = self.filter(sitio__id=sitio_id).aggregate(
            fecha_carga_max=models.Max('fecha_carga')
        )['fecha_carga_max']
        return self.filter(fecha_carga=latest_date)\
            if latest_date else self.none()


class ComentarioManager(models.Manager):
    def for_sitio(self, sitio_id):
        # Filtra los comentarios de un sitio específico
        return self.filter(sitio__id=sitio_id).order_by('fecha_carga')

    def latest_for_sitio(self, sitio_id):
        # Obtiene los comentarios más recientes para un sitio específico
        latest_date = self.filter(sitio__id=sitio_id).aggregate(
            fecha_carga_max=models.Max('fecha_carga')
        )['fecha_carga_max']
        return self.filter(fecha_carga=latest_date)\
            if latest_date else self.none()
