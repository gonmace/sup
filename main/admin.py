from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Chat, Contratista, Mensaje, Sitio, UserProfile
# from django.utils.dateformat import format


class SitiosResource(resources.ModelResource):
    sitio = fields.Field(column_name='Site ID', attribute='sitio')
    cod_id = fields.Field(column_name='Client ID', attribute='cod_id')
    nombre = fields.Field(column_name='Name Site', attribute='nombre')
    altura = fields.Field(column_name='ESA Height', attribute='altura')
    contratista = fields.Field(
        column_name='Partner', attribute='contratista',
        widget=ForeignKeyWidget(Contratista, 'name'))
    lat = fields.Field(column_name='LAT', attribute='lat')
    lon = fields.Field(column_name='LON', attribute='lon')
    ito = fields.Field(
        column_name='ITO', attribute='ito',
        widget=ForeignKeyWidget(UserProfile, 'user'))

    class Meta:
        model = Sitio
        fields = (
            'sitio',
            'cod_id',
            'nombre',
            'altura',
            'contratista',
            'lat',
            'lon',
            'ito',
        )
        import_id_fields = ('sitio',)


class SitioAdmin(ImportExportModelAdmin):
    resource_class = SitiosResource
    list_display = (
        'sitio',
        'cod_id',
        'nombre',
        'altura',
        'contratista',
        'ito',
        'estado',
        'proyecto',
    )
    list_editable = ('ito', 'contratista', 'estado', 'proyecto')
    list_display_links = ('sitio', )
    list_filter = ('contratista', 'estado', 'proyecto', 'ito')


admin.site.register(Sitio, SitioAdmin)

admin.site.register(Contratista)


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 1
    fields = ('usuario', 'mensaje', 'datetime')
    readonly_fields = ('datetime', )


class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sitio',
        'activar',
    )
    list_editable = ('activar',)
    inlines = [MensajeInline]


admin.site.register(Chat, ChatAdmin)
