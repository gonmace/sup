# Generated by Django 5.1.1 on 2024-10-11 01:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0006_delete_progresoactividad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progreso',
            name='proyecto_actividad',
        ),
        migrations.AddField(
            model_name='progreso',
            name='progreso',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='actividades.proyectoactividad'),
            preserve_default=False,
        ),
    ]
