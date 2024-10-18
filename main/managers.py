from django.db import models


class SitioManager(models.Manager):
    def for_user_profile(self, user_profile):
        # Filtrar los sitios en base al perfil de usuario
        if user_profile.cargo == 'SUP':
            return self.filter(ito=user_profile)
        else:
            return self.filter(proyecto__in=user_profile.proyectos.all())


class ContratistaManager(models.Manager):
    def for_sitios(self, sitios):
        # Filtrar los contratistas asociados con los sitios
        return self.filter(sitio__in=sitios).distinct()
