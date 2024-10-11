# Generated by Django 5.1.1 on 2024-10-11 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0007_remove_progreso_proyecto_actividad_progreso_progreso'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleProgreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('actividad_grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.actividadgrupo')),
                ('progreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='actividades.progreso')),
            ],
            options={
                'verbose_name': 'Detalle de Progreso',
                'verbose_name_plural': 'Detalles de Progresos',
            },
        ),
    ]
