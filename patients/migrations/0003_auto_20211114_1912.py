# Generated by Django 3.2.6 on 2021-11-14 19:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_auto_20211114_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdv',
            name='date_rdv',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='DATE DU RDV'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rdv',
            name='heure_rdv',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='HEURE DU RDV'),
            preserve_default=False,
        ),
    ]