# Generated by Django 5.1.1 on 2024-10-16 22:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0018_alter_detalleprogreso_options_detalleprogreso_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyectoactividad',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]