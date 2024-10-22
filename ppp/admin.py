# An example admin.py for a Table of Contents app

from django.contrib import admin
import nested_admin

from .models import Bloque, Imagen, Card, Proyecto


class CardInline(nested_admin.NestedStackedInline):
    model = Card
    sortable_field_name = "orden"


class ImagenInline(nested_admin.NestedStackedInline):
    model = Imagen
    sortable_field_name = "orden"
    extra = 1


class BloquesAdmin(nested_admin.NestedModelAdmin):
    inlines = [CardInline, ImagenInline]


admin.site.register(Bloque, BloquesAdmin)

admin.site.register(Proyecto)