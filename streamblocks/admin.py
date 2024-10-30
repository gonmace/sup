# admin.py
from django.contrib import admin
from streamfield.fields import StreamFieldWidget
from .models import (
    ProyectoComponentes,
    MessageWithIcon,
    RadialProgress,
    Text,
    ImageWithText,
    OpenUrl
    )


@admin.register(ProyectoComponentes)
class PageAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.id == 1:
            form.base_fields['stream'].widget = StreamFieldWidget(
                attrs={'model_list': [
                    Text,
                    ImageWithText,
                    OpenUrl,
                    MessageWithIcon,
                    RadialProgress,
                    ]})
        return form
