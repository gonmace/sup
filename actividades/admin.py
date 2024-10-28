from django.contrib import admin

from clientes.models import UserProfile
from .models import (
    Actividad,
    DetalleProgreso,
    GrupoActividades,
    ActividadGrupo,
    Progreso,
    ProyectoActividad
    )
from adminsortable2.admin import SortableAdminBase, SortableTabularInline


class ActividadGrupoInline(SortableTabularInline):
    model = ActividadGrupo
    extra = 0
    fields = ['id', 'actividad', 'ponderacion', 'order']
    readonly_fields = ('id', )


@admin.register(GrupoActividades)
class GrupoActividadesAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ActividadGrupoInline]
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


class DetalleProgresoInline(SortableTabularInline):
    model = DetalleProgreso
    extra = 0
    max_num = 0
    fields = (
        'actividad_grupo',
        'porcentaje',
        'mostrar',
        'fecha_actualizacion'
        )
    readonly_fields = ('id', 'fecha_actualizacion', 'actividad_grupo')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Asegurarse de usar la instancia correcta de UserProfile
        user_profile = UserProfile.objects.get(user=request.user)
        return qs.filter(progreso__proyecto__ito=user_profile)


class ProgresoAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('progreso', 'activar', )
    list_editable = ('activar',)
    inlines = [
        DetalleProgresoInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Asegurarse de usar la instancia correcta de UserProfile
        user_profile = UserProfile.objects.get(user=request.user)
        return qs.filter(progreso__proyecto__ito=user_profile)


admin.site.register(Progreso, ProgresoAdmin)


class ProyectoActividadAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'grupo', 'fecha_creacion_formateada')

    def fecha_creacion_formateada(self, obj):
        # Formatear la fecha en el formato deseado
        return obj.fecha_creacion.strftime('%d-%b-%Y')

    fecha_creacion_formateada.short_description = 'Fecha de Creación'


admin.site.register(ProyectoActividad, ProyectoActividadAdmin)
