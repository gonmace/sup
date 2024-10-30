from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mensaje
from channels.layers import get_channel_layer  # Importa get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Mensaje)
def mensaje_saved(sender, instance, created, **kwargs):
    message = {
        'chat': instance.chat.id,
        'id': instance.id,
        'text': instance.mensaje,
        # 'author': instance.usuario,
        'type': 'created' if created else 'updated'
    }
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        'chat_mensajes',
        {
            'type': 'chat_message',
            'message': message
        }
    )


@receiver(post_delete, sender=Mensaje)
def mensaje_deleted(sender, instance, **kwargs):
    message = {
        'chat': instance.chat.id,
        'id': instance.id,
        'type': 'deleted'
    }
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        'chat_mensajes',
        {
            'type': 'chat_message',
            'message': message
        }
    )
