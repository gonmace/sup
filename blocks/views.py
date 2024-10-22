from django.contrib import admin
from .models import Pagina, Tarjeta, Imagen
from adminsortable2.admin import SortableInlineAdminMixin


class TarjetaInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Tarjeta
    extra = 1


class ImagenInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Imagen
    extra = 1


class PaginaAdmin(admin.ModelAdmin):
    inlines = [TarjetaInline, ImagenInline]
    # Añade más inlines si tienes más tipos de bloques


admin.site.register(Pagina, PaginaAdmin)
