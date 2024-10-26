# # streamblocks/admin.py

# from django.contrib import admin
# from streamfield.admin import StreamBlocksAdmin

# from streamblocks.models import Text

# admin.site.unregister(Text)


# @admin.register(Text)
# class RichTextBlockAdmin(StreamBlocksAdmin, admin.ModelAdmin):
#     pass

# from django.contrib import admin
# from .models import Text

# class TextAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # Si el objeto es nuevo
# (no tiene una clave primaria todavía)
#             obj.user = request.user  # Asigna el usuario actual
#         super().save_model(request, obj, form, change)

# admin.site.register(Text, TextAdmin)
