# Generated by Django 5.1.1 on 2024-10-11 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0004_alter_proyectoactividad_proyecto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Progreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto_actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.proyectoactividad')),
            ],
        ),
        migrations.CreateModel(
            name='ProgresoActividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_personalizado', models.BooleanField(default=False)),
                ('actividad_grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.actividadgrupo')),
                ('progreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.progreso')),
            ],
        ),
    ]
