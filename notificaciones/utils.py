# main/utils.py

from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

def send_test_notification(user):
    # Filtra los dispositivos asociados al usuario y asegúrate de que el tipo sea 'web'
    devices = FCMDevice.objects.filter(user=user, type='web')
    
    # Define el mensaje de la notificación
    message = Message(
        notification=Notification(
            title="Notificación de Prueba",
            body="Este es un mensaje de prueba"
        ),
        data={
            "key1": "value1",
            "key2": "value2"
        }
    )
    
    # Enviar la notificación
    devices.send_message(message)
