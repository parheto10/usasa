# Generated by Django 3.2.6 on 2021-11-14 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_auto_20211114_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdv',
            name='date_rdv',
            field=models.DateField(blank=True, verbose_name='DATE DU RDV'),
        ),
    ]