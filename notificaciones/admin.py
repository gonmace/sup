# notificaciones/admin.py
from django.contrib import admin
from .models import SendNotificacionPush, UsuarioNotificacion


@admin.register(UsuarioNotificacion)
class UsuariosNotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_notificacion', 'device_id')
    list_editable = ('tipo_notificacion',)

    def device_id(self, obj):
        return obj.usuario.device_id
    device_id.short_description = 'Device ID'


@admin.register(SendNotificacionPush)
class SendNotificacionPushAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_creacion')
    filter_horizontal = ('usuarios',)
