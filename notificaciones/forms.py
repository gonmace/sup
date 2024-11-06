from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import SuscripcionNotificacion


class SuscripcionNotificacionForm(forms.ModelForm):
    class Meta:
        model = SuscripcionNotificacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones de 'modelo' para que solo incluya
        # los modelos en ALLOWED_MODELS
        allowed_content_types = ContentType.objects.filter(
            model__in=[model.split('.')[1].lower()
                       for model in SuscripcionNotificacion.ALLOWED_MODELS],
            app_label__in=[model.split('.')[0]
                           for model in SuscripcionNotificacion.ALLOWED_MODELS]
        )
        self.fields['modelo'].queryset = allowed_content_types
