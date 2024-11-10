from django.contrib import admin
from clientes.models import Cliente, LogoRedLine, Proyecto, UserProfile
from django.utils.html import format_html
from django.utils.html import mark_safe


@admin.register(LogoRedLine)
class LogoRedLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_thumbnail')

    def logo_thumbnail(self, obj):
        if obj.logo:
            return mark_safe(f'<img class="sombra contenedor" src="{obj.logo.url}" style="height: 40px;">')
        return "-"
    logo_thumbnail.short_description = 'Logo Preview'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cod', 'logo_thumbnail')

    def logo_thumbnail(self, obj):
        if obj.logo_mostrar:
            return mark_safe(f'<img src="{obj.logo_mostrar.logo.url}" style="background-color: white; height: 25px;">')
        return "-"
    logo_thumbnail.short_description = 'Logo a Mostra al Cliente'


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cod', 'cliente')


admin.site.register(Proyecto, ProyectoAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'cliente','cargo', 'get_proyectos')
    list_editable = ('cargo', 'cliente')

    def get_username(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_username.short_description = 'Nombre'

    def get_proyectos(self, obj):
        proyectos = [proyecto.cod for proyecto in obj.proyectos.all()]
        return format_html("<br>".join(proyectos))
    get_proyectos.short_description = 'Proyectos'
    get_proyectos.allow_tags = True


admin.site.register(UserProfile, UserProfileAdmin)
