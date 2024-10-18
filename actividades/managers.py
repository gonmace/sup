from django.db import models


class ProgresoManager(models.Manager):
    def get_active_for_sitio(self, sitio_id):
        # Obtener el progreso activado para un sitio específico
        try:
            progreso = self.get(progreso__proyecto__id=sitio_id, activar=True)
            return progreso
        except self.model.DoesNotExist:
            return None


class DetalleProgresoManager(models.Manager):
    def for_progreso(self, progreso):
        # Filtrar detalles de progreso que deben ser mostrados
        # y están relacionados con un progreso específico
        return self.filter(progreso=progreso, mostrar=True).select_related(
            'actividad_grupo', 'actividad_grupo__actividad'
        )
