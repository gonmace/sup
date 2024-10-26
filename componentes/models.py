# from django.conf import settings
# from django.db import models
# # models.py
# from streamfield.fields import StreamField
# from streamblocks.models import Text, ImageWithText
# from main.models import Sitio
from django.db import models
from streamfield.fields import StreamField
from main.models import Sitio
from streamblocks.models import Text, ImageWithText


class ProyectoComponentes(models.Model):
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    stream = StreamField(
        model_list=[
            Text,
            ImageWithText
        ],
        verbose_name="Componentes",
        )

    def __str__(self):
        return str(self.sitio)
