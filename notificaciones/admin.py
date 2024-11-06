# notificaciones/admin.py
from django.contrib import admin
from .forms import SuscripcionNotificacionForm
from .models import NotificacionPush, SuscripcionNotificacion


@admin.register(NotificacionPush)
class NotificacionPushAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_creacion')
    filter_horizontal = ('usuarios',)


@admin.register(SuscripcionNotificacion)
class SuscripcionNotificacionAdmin(admin.ModelAdmin):
    form = SuscripcionNotificacionForm
    list_display = ('modelo', 'fecha_creacion')
    filter_horizontal = ('usuarios',)
    list_display_links = ('modelo',)
