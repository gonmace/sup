from django import forms

from clientes.models import UserProfile
from main.models import Sitio
from .models import Imagen


class SitioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Mostrar sitio junto con cod_id y nombre
        return f"{obj.sitio} | {obj.cod_id if obj.cod_id else ''} | \
            {obj.nombre if obj.nombre else ''}"


class ImagesForm(forms.ModelForm):
    # Aquí agregas un campo extra para el comentario,
    # este no está vinculado directamente a un modelo
    comentario = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Imagen
        fields = ['sitio', 'fecha_carga', 'comentario']

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)  # Capturamos el usuario de kwargs
        super(ImagesForm, self).__init__(*args, **kwargs)

        # Reemplazamos el campo sitio con nuestro campo
        # personalizado SitioChoiceField
        self.fields['sitio'] = SitioChoiceField(
            queryset=Sitio.objects.none(),
            required=True
        )

        # Asegurarnos de que el usuario se pase correctamente
        if user:
            try:
                user_profile = user.userprofile_set.first()

                if user_profile and user_profile.cargo == 'SUP':
                    self.fields['sitio'].queryset = Sitio.objects.filter(
                        ito=user_profile)
                elif user_profile:
                    self.fields['sitio'].queryset = Sitio.objects.filter(
                        proyecto__in=user_profile.proyectos.all())
                else:
                    # No tiene perfil
                    self.fields['sitio'].queryset = Sitio.objects.none()
            except UserProfile.DoesNotExist:
                self.fields['sitio'].queryset = Sitio.objects.none()
        else:
            self.fields['sitio'].queryset = Sitio.objects.none()
