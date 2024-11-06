# notificaciones/views.py
import os
import json
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.http import HttpResponse, JsonResponse, FileResponse
from fcm_django.models import FCMDevice
from django.views.decorators.csrf import csrf_exempt


def firebase_logo(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'firebase-logo.png')
    return FileResponse(open(file_path, 'rb'), content_type='image/png')


# PUSH NOTIFICATION
@never_cache
def service_worker(request):
    # Ubicación del archivo del Service Worker
    sw_path = os.path.join(
        settings.BASE_DIR, 'notificaciones', 'firebase-messaging-sw.js')
    with open(sw_path, 'r') as sw_file:
        response = HttpResponse(
            sw_file.read(), content_type='application/javascript')
    return response


@csrf_exempt
def save_token(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            token = data.get('fcm_token')
            device_OS = data.get('device_os')

            # Almacena el token asociado al usuario autenticado
            if token:
                device, created = FCMDevice.objects.get_or_create(
                    registration_id=token,
                    defaults={
                        'user': request.user,  # Asocia el usuario autenticado
                        'name': request.user.username,
                        'device_id': device_OS,
                        'type': 'web'
                    }
                )
                # Si el dispositivo ya existe,
                # actualiza el usuario y el nombre si es necesario
                if not created:
                    device.user = request.user
                    device.name = request.user.username
                    device.save()

                return JsonResponse({'message': 'Token guardado exitosamente'})
            else:
                return JsonResponse(
                    {'message': 'Token no proporcionado'}, status=400)
        else:
            return JsonResponse({'message': 'Método no permitido'}, status=405)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        print(f"Error en la vista save_token: {e}")
        return JsonResponse(
            {'message': 'Error interno en el servidor'}, status=500)
