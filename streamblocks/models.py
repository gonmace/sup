from django.db import models
from django.conf import settings



TEXT_BORDER_CHOICES = (
    ("rojo", "Rojo"),
    ("amarillo", "Amarillo"),
    ("verde", "Verde"),
)


class Text(models.Model):
    title = models.CharField("Titulo", max_length=100, blank=True, null=True)
    text = models.TextField("Texto", blank=True, null=True)
    border = models.CharField(
        "Color de borde",
        max_length=10,
        choices=TEXT_BORDER_CHOICES,
        blank=True,
        null=True
        )
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name="texto_block",
    #     # editable=False,
    #     blank=True,
    #     null=True
    # )
    user_show = models.BooleanField("Firma de Usuario", default=True)

    def __str__(self):
        if self.title:
            return f"{self.title} | {self.text[:30]}"
        return self.text[:30]

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"


class ImageWithText(models.Model):
    image = models.ImageField(upload_to="folder/")
    text = models.TextField(null=True, blank=True)

    # StreamField option for list of objects
    as_list = True

    def __str__(self):
        # This text will be added to block title name.
        # For better navigation when block is collapsed.
        return self.text[:30]

    class Meta:
        verbose_name = "Image with text"
        verbose_name_plural = "Images with text"


# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    Text,
    ImageWithText
]
