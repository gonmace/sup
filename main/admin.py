from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import Contratista, Sitio, Supervisor
from django.contrib import admin
from import_export.widgets import ForeignKeyWidget


class SitiosResource(resources.ModelResource):
    sitio = fields.Field(column_name='Site ID', attribute='sitio')
    cod_id = fields.Field(column_name='Client ID', attribute='cod_id')
    nombre = fields.Field(column_name='Name Site', attribute='nombre')
    altura = fields.Field(column_name='ESA Height', attribute='altura')
    contratista = fields.Field(
        column_name='Partner',
        attribute='contratista',
        widget=ForeignKeyWidget(Contratista, 'name')
    )
    lat = fields.Field(column_name='LAT', attribute='lat')
    lon = fields.Field(column_name='LON', attribute='lon')
    ito = fields.Field(
        column_name='ITO',
        attribute='ito',
        widget=ForeignKeyWidget(Supervisor, 'name')
        )

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


# @admin.register(Sitio)
class SitioAdmin(ImportExportModelAdmin):
    resource_class = SitiosResource
    list_display = (
        'sitio',
        'cod_id',
        'nombre',
        'altura',
        'contratista',
        'ito',
    )
    list_editable = ('ito',)
    list_display_links = ('sitio', )


admin.site.register(Sitio, SitioAdmin)

admin.site.register(Contratista)

admin.site.register(Supervisor)
