# Generated by Django 5.1.1 on 2024-10-08 01:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_supervisor_options_alter_sitio_cod_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('ASG', 'Asignado'), ('EJE', 'Ejecución'), ('TER', 'Terminado'), ('PTG', 'Postergado'), ('CAN', 'Cancelado')], default='EJE', max_length=3, verbose_name='Estado')),
                ('excavacion', models.DateField(blank=True, null=True, verbose_name='Excavación')),
                ('hormigonado', models.DateField(blank=True, null=True, verbose_name='Hormigonado')),
                ('montaje', models.DateField(blank=True, null=True, verbose_name='Montaje')),
                ('energia_prov', models.DateField(blank=True, null=True, verbose_name='Energía Provisional')),
                ('energia_def', models.DateField(blank=True, null=True, verbose_name='Energía Definitiva')),
                ('porcentaje', models.FloatField(default=0.0, verbose_name='Porcentaje')),
                ('fecha_fin', models.DateField(blank=True, null=True, verbose_name='Fecha Fin')),
                ('comentario', models.TextField(blank=True, null=True, verbose_name='Comentarios')),
                ('sitio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.sitio')),
            ],
            options={
                'verbose_name': 'Avance',
                'verbose_name_plural': 'Avance Proyectos',
            },
        ),
    ]
