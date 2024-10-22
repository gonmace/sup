from django.contrib import admin
from .models import Imagen, Comentario
from django.utils.html import format_html


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'sitio', 'pic_tag', 'fecha_carga',  'descripcion', 'usuario'
        )
    list_editable = ('descripcion', 'fecha_carga', 'usuario')
    search_fields = ('sitio__sitio', 'fecha_carga')

    def pic_tag(self, obj):
        return format_html(
            '<img src="{}" style="max-height: 100px;">'.format(obj.imagen.url)
            )

    pic_tag.short_description = 'Imagen'


admin.site.register(Imagen, ImageAdmin)

admin.site.register(Comentario)
