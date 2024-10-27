# views.py
from django.shortcuts import get_object_or_404
from .models import ProyectoComponentes
from django.http import JsonResponse
from django.template.loader import render_to_string


def render_streamfield(request, sitio_pk):
    proyecto = get_object_or_404(
        ProyectoComponentes, sitio__pk=sitio_pk
        )
    # # Asignar el usuario si el proyecto no tiene uno asociado
    # if proyecto.user is None:
    #     proyecto.user = request.user
    #     proyecto.save()

    stream_html = render_to_string(
        'proyecto_componentes.html', {
            'proyecto': proyecto,
            }
        )
    return JsonResponse({'html': stream_html})
