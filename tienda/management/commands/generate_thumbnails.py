from django.core.management.base import BaseCommand
from tienda.models import Accesorio
from PIL import Image
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Genera thumbnails para las imágenes de accesorios.'

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(settings.MEDIA_ROOT, 'accesorios')
        thumb_dir = os.path.join(base_dir, 'thumbnails')
        os.makedirs(thumb_dir, exist_ok=True)
        count = 0
        for accesorio in Accesorio.objects.exclude(imagen=''):
            if not accesorio.imagen:
                continue
            orig_path = accesorio.imagen.path
            filename = os.path.basename(orig_path)
            thumb_path = os.path.join(thumb_dir, filename)
            if os.path.exists(thumb_path):
                continue
            try:
                with Image.open(orig_path) as img:
                    img.thumbnail((320, 320))
                    img.save(thumb_path, format=img.format, quality=80)
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Thumbnail creado: {filename}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error con {filename}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Thumbnails generados: {count}'))
