from django.contrib import admin

# admin.py
from streamfield.fields import StreamFieldWidget
from streamblocks.models import Text, ImageWithText
from .models import ProyectoComponentes


@admin.register(ProyectoComponentes)
class PageAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.id == 1:
            form.base_fields['stream'].widget = StreamFieldWidget(
                attrs={'model_list': [
                    Text,
                    # Card,
                    ImageWithText]})
        return form
