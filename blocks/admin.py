from django.contrib import admin
from polymorphic.admin import (
    PolymorphicInlineSupportMixin,
    StackedPolymorphicInline,
)
from .models import Proyecto, Bloque, Card, Imagen


class CardInline(StackedPolymorphicInline.Child):
    model = Card
    fields = ('orden', 'nombre', 'titulo', 'descripcion')
    extra = 1


class ImagenInline(StackedPolymorphicInline.Child):
    model = Imagen
    fields = ('orden', 'nombre', 'archivo_imagen')
    extra = 1


class BloqueInline(StackedPolymorphicInline):
    model = Bloque
    child_inlines = (
        CardInline,
        ImagenInline,
    )
    fields = ('orden', 'nombre')
    extra = 0


@admin.register(Proyecto)
class ProyectoAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = [BloqueInline]
    list_display = ('titulo',)

