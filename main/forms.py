from django import forms
from .models import Mensaje, Sitio
from django.core.exceptions import ValidationError


class MensajeForm(forms.ModelForm):
    sitio_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
        )

    class Meta:
        model = Mensaje
        fields = ['mensaje', 'sitio_id']

    def clean_sitio_id(self):
        sitio_id = self.cleaned_data.get('sitio_id')
        try:
            Sitio.objects.get(pk=sitio_id)
        except Sitio.DoesNotExist:
            raise ValidationError(
                "No existe un sitio con el ID proporcionado."
                )
        return sitio_id
