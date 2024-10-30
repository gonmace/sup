# Ubica este script en el directorio de tu aplicación de Django
import os
from django.core.management.base import BaseCommand
from PIL import Image
from galeria.models import Imagen  # Cambia 'myapp' al nombre de tu aplicación


class Command(BaseCommand):
    help = 'Convertir todas las imágenes existentes a formato WebP'

    def handle(self, *args, **options):
        images = Imagen.objects.all()
        for image in images:
            self.stdout.write(
                self.style.SUCCESS(f'Procesando imagen: {image.imagen.name}')
                )
            self.convert_to_webp(image)

    def convert_to_webp(self, image):
        if image.imagen:
            original_path = image.imagen.path
            webp_path = f"{original_path.rsplit('.', 1)[0]}.webp"

            # Comprobar si el archivo WebP ya existe
            if not os.path.exists(webp_path):
                img = Image.open(original_path)
                img.save(webp_path, "WEBP", quality=50)
                self.stdout.write(
                    self.style.SUCCESS(f'Guardada WebP: {webp_path}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Archivo WebP ya existe: {webp_path}'))
