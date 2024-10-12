from django.contrib import admin
from .models import (
    Actividad,
    DetalleProgreso,
    GrupoActividades,
    ActividadGrupo,
    Progreso,
    ProyectoActividad
    )


class ActividadGrupoInline(admin.TabularInline):
    model = ActividadGrupo
    extra = 1  # Cantidad de filas adicionales para agregar actividades
    fields = ['actividad', 'ponderacion']  # Mostrar solo actividad y número


@admin.register(GrupoActividades)
class GrupoActividadesAdmin(admin.ModelAdmin):
    inlines = [ActividadGrupoInline]
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


class DetalleProgresoInline(admin.TabularInline):
    model = DetalleProgreso
    extra = 0
    max_num = 0


class ProgresoAdmin(admin.ModelAdmin):
    list_display = ('progreso', 'activar')
    list_editable = ('activar',)
    inlines = [
        DetalleProgresoInline,
    ]


admin.site.register(Progreso, ProgresoAdmin)

admin.site.register(ProyectoActividad)
