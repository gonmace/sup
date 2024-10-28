
from django.contrib import admin

from clientes.models import UserProfile
from .models import Imagen, Comentario, Icon
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'sitio', 'pic_tag', 'fecha_carga',  'descripcion', 'usuario'
        )
    list_editable = ('descripcion', 'fecha_carga', 'usuario')
    search_fields = ('sitio__sitio', 'fecha_carga')

    def pic_tag(self, obj):
        webp_url = obj.imagen.url.rsplit('.', 1)[0] + '.webp'
        return format_html(
            '<img src="{}" style="max-height: 100px;">'.format(webp_url)
            )

    pic_tag.short_description = 'Imagen'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Asumiendo que UserProfile es una extensión de User 
        # y que cada usuario tiene un UserProfile asociado
        user_profile = UserProfile.objects.get(user=request.user)
        return qs.filter(sitio__ito=user_profile)


admin.site.register(Imagen, ImageAdmin)


class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('sitio', 'comentario', 'fecha_carga', 'usuario')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Asumiendo que UserProfile es una extensión de User
        # y que cada usuario tiene un UserProfile asociado
        user_profile = UserProfile.objects.get(user=request.user)
        return qs.filter(sitio__ito=user_profile)


admin.site.register(Comentario, ComentarioAdmin)
# admin.site.register(Comentario)


class IconAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_icon')
    readonly_fields = ['display_icon']

    def display_icon(self, obj):
        svg_html = mark_safe(obj.icon)

        return format_html(
            '<div style="width: 25px; height: 25px;">{}</div>', svg_html
            )
    display_icon.short_description = "Vista Previa del Icono"


admin.site.register(Icon, IconAdmin)
