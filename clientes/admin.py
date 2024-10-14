from django.contrib import admin
from clientes.models import Cliente, Proyecto, UserProfile
from django.utils.html import format_html


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cod')


admin.site.register(Cliente, ClienteAdmin)


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cod', 'cliente')


admin.site.register(Proyecto, ProyectoAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'cargo', 'get_proyectos')
    list_editable = ('cargo', )

    def get_username(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_username.short_description = 'Nombre'

    def get_proyectos(self, obj):
        proyectos = [proyecto.cod for proyecto in obj.proyectos.all()]
        return format_html("<br>".join(proyectos))
    get_proyectos.short_description = 'Proyectos'
    get_proyectos.allow_tags = True


admin.site.register(UserProfile, UserProfileAdmin)
