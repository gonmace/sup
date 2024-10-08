from django.shortcuts import render
from main.models import Sitio, Avance
import json


def home(request):
    sitios = Sitio.objects.all()
    sitios_data = []
    for sitio in sitios:
        # Obtenemos los datos del sitio
        sitio_data = {
            'id': sitio.id,
            'sitio': sitio.sitio,
            'cod_id': sitio.cod_id,
            'nombre': sitio.nombre,
            'altura': sitio.altura,
            'lat': sitio.lat,
            'lon': sitio.lon,
            'contratista': sitio.contratista.nombre
            if sitio.contratista else None,
            'ito': sitio.ito.nombre if sitio.ito else None,
            # Agrega otros campos si es necesario
        }

        # Intentamos obtener el avance relacionado
        try:
            # Gracias al OneToOneField, podemos acceder directamente
            avance = sitio.avance
            avance_data = {
                'estado': avance.estado,
                'excavacion': avance.excavacion.strftime('%Y-%m-%d')
                if avance.excavacion else None,

                'hormigonado': avance.hormigonado.strftime('%Y-%m-%d')
                if avance.hormigonado else None,

                'montado': avance.montaje.strftime('%Y-%m-%d')
                if avance.montaje else None,

                'energia_prov': avance.ener_prov.strftime('%Y-%m-%d')
                if avance.ener_prov else None,

                'energia_def': avance.ener_def.strftime('%Y-%m-%d')
                if avance.ener_def else None,

                'porcentaje': avance.porcentaje,
                'fecha_fin': avance.fecha_fin.strftime('%Y-%m-%d')
                if avance.fecha_fin else None,

                'comentario': avance.comentario,
            }
        except Avance.DoesNotExist:
            # Si no existe un avance asociado
            avance_data = None

        # Agregamos el avance al sitio
        sitio_data['avance'] = avance_data

        sitios_data.append(sitio_data)

    sitios_json = json.dumps(sitios_data)

    context = {
        'sitios_json': sitios_json,
    }
    return render(request, 'home_page.html', context)

