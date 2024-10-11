# from django.http import JsonResponse
# from .models import GrupoActividades, ActividadGrupo


# def get_actividades_por_grupo(request):
#     grupo_id = request.GET.get('grupo_id')
#     actividades_data = []

#     if grupo_id:
#         grupo = GrupoActividades.objects.get(id=grupo_id)
#         actividades_grupo = ActividadGrupo.objects.filter(grupo=grupo)

#         for actividad_grupo in actividades_grupo:
#             actividades_data.append({
#                 'id': actividad_grupo.id,
#                 'nombre': actividad_grupo.actividad.nombre,
#             })

#     return JsonResponse({'actividades': actividades_data})
