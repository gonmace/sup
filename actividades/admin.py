from django.contrib import admin
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


class ProgresoAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('progreso', 'activar')
    list_editable = ('activar',)
    inlines = [
        DetalleProgresoInline,
    ]


admin.site.register(Progreso, ProgresoAdmin)


class ProyectoActividadAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'grupo', 'fecha_creacion_formateada')

    def fecha_creacion_formateada(self, obj):
        # Formatear la fecha en el formato deseado
        return obj.fecha_creacion.strftime('%d-%b-%Y')

    fecha_creacion_formateada.short_description = 'Fecha de Creación'


admin.site.register(ProyectoActividad, ProyectoActividadAdmin)
