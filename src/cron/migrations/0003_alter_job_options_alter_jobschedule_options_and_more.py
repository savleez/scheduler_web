# Generated by Django 4.2.4 on 2023-08-26 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cron', '0002_alter_job_id_alter_jobschedule_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['name'], 'verbose_name': 'Job', 'verbose_name_plural': 'Jobs'},
        ),
        migrations.AlterModelOptions(
            name='jobschedule',
            options={'ordering': ['job', 'description'], 'verbose_name': 'Horario de Job', 'verbose_name_plural': 'Horarios de Jobs'},
        ),
        migrations.AlterField(
            model_name='jobschedule',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Descripción'),
        ),
    ]
