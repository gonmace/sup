from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Contratista, Sitio, Supervisor, Avance
from django.utils.dateformat import format


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
        widget=ForeignKeyWidget(Supervisor, 'name'))

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
    )
    list_editable = ('ito', 'contratista')
    list_display_links = ('sitio', )


admin.site.register(Sitio, SitioAdmin)

admin.site.register(Contratista)

admin.site.register(Supervisor)


class AvanceResource(resources.ModelResource):
    sitio = fields.Field(
        column_name='Site ID',
        attribute='sitio',
        widget=ForeignKeyWidget(Sitio, 'sitio'))
    estado = fields.Field(column_name='Estado', attribute='estado')
    excavacion = fields.Field(column_name='EXCAVACION', attribute='excavacion')
    hormigonado = fields.Field(
        column_name='HORMIGONADO', attribute='hormigonado')
    montaje = fields.Field(column_name='MONTAJE TORRE', attribute='montaje')
    ener_prov = fields.Field(column_name='ENERGIA PROV', attribute='ener_prov')
    ener_def = fields.Field(column_name='ENERGIA DEF', attribute='ener_def')
    porcentaje = fields.Field(column_name='AVANCE', attribute='porcentaje')
    fecha_fin = fields.Field(
        column_name='CIERRE PERIMETRAL Y OBRAS ADICIONALES',
        attribute='fecha_fin')
    comentario = fields.Field(
        column_name='ESTADO ACTUAL', attribute='comentario')

    class Meta:
        model = Avance
        fields = ()
        export_order = (
            'sitio',
            'estado',
            'excavacion',
            'hormigonado',
            'montado',
            'empalmeE',
            'porcentaje',
            'fechaFin',
            'comentario',
        )
        import_id_fields = ('sitio',)


# @admin.register(Avance)
class AvanceAdmin(ImportExportModelAdmin):
    resource_class = AvanceResource
    list_display = (
        'sitio',
        'display_cod_id',
        'display_nombre',
        'estado',
        'formato_excavacion',
        'formato_hormigonado',
        'formato_montado',
        'formato_ener_prov',
        'formato_ener_def',
        'porcentaje',
        'formato_fecha_final',
        'comentario',
    )
    list_editable = (
        'estado',
        'porcentaje',
        'comentario',
    )
    list_display_links = ('sitio', )

    def display_cod_id(self, obj):
        # Accede al campo cod_id del modelo Sitio relacionado
        return obj.sitio.cod_id
    display_cod_id.short_description = 'Cod ID'

    def display_nombre(self, obj):
        # Accede al campo entel_id del modelo Sitio relacionado
        return obj.sitio.nombre
    display_cod_id.short_description = 'Nombre'

    def formato_excavacion(self, obj):
        return self.formato_fecha(obj.excavacion)
    formato_excavacion.short_description = 'Excavación'

    def formato_hormigonado(self, obj):
        return self.formato_fecha(obj.hormigonado)
    formato_hormigonado.short_description = 'Hormigonado'

    def formato_montado(self, obj):
        return self.formato_fecha(obj.montaje)
    formato_montado.short_description = 'Montado'

    def formato_ener_prov(self, obj):
        return self.formato_fecha(obj.ener_prov)
    formato_ener_prov.short_description = 'Energia Prov.'

    def formato_ener_def(self, obj):
        return self.formato_fecha(obj.ener_def)
    formato_ener_def.short_description = 'Energia Def.'

    def formato_fecha_final(self, obj):
        return self.formato_fecha(obj.fecha_fin)
    formato_fecha_final.short_description = 'Fecha Final'

    def formato_fecha(self, fecha):
        if fecha:
            return format(fecha, 'd/m/Y')  # Formatea la fecha como dd/mm/YY
        return '---'


admin.site.register(Avance, AvanceAdmin)
