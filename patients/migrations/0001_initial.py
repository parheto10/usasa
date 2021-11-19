# Generated by Django 3.2.6 on 2021-11-13 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parametres', '0002_auto_20211113_0433'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_patient', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='NUMERO')),
                ('genre', models.CharField(blank=True, choices=[('H', 'HOMMME'), ('F', 'FEMME')], default='H', max_length=10, null=True, verbose_name='GENRE')),
                ('dob', models.DateField(verbose_name='Date de Naissance')),
                ('poids', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('groupe_sanguin', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], default='A+', max_length=3, null=True, verbose_name='GROUPE SANGUIN')),
                ('telephone1', models.CharField(help_text='Veuillez entrer un Numero Au format International Exple: +225 xx xx xx xx xx', max_length=50, verbose_name='TELEPHONE 1')),
                ('telephone2', models.CharField(blank=True, max_length=50, null=True, verbose_name='TELEPHONE 2')),
                ('adresse', models.CharField(blank=True, max_length=255, null=True, verbose_name='ADRESSE')),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload_image')),
                ('details', models.TextField(blank=True, null=True, verbose_name='Historique Médical')),
                ('nb_consultation', models.PositiveIntegerField(default=0, verbose_name='NOMBRE DE CONSULTATION')),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('pays', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parametres.pays')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'patient',
                'verbose_name_plural': 'PATIENTS',
                'ordering': ['-add_le'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix', models.PositiveIntegerField(blank=True, default=0)),
                ('nb_consultation', models.PositiveIntegerField(blank=True, default=0)),
                ('is_abonne', models.BooleanField(default=False, verbose_name='ABONNEMENT')),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('abonnement', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='abonnement_formule', to='parametres.abonnement')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonnement_patient', to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Rdv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, help_text='LE CODE RDV EST GENERE AUTOMATIQUEMENT', max_length=150, verbose_name='CODE RDV')),
                ('date_rdv', models.DateField(verbose_name='DATE DU RDV')),
                ('heure_rdv', models.TimeField(verbose_name='HEURE DU RDV')),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('prenoms', models.CharField(blank=True, max_length=255, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('age', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('poids', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('taille', models.PositiveIntegerField(blank=True, default=0, verbose_name='Taille(cm)')),
                ('ta', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='TENSION ARTERIELLE(TA)')),
                ('poults', models.PositiveIntegerField(default=0)),
                ('systolique', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('diastolique', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('nb_rdv', models.PositiveIntegerField(default=0)),
                ('is_ok', models.BooleanField(default=False)),
                ('alert', models.CharField(choices=[('APPEL', 'APPEL'), ('EMAIL', 'EMAIL'), ('SMS', 'SMS')], default='EMAIL', max_length=100, verbose_name='ALERT RDVS')),
                ('last_examen', models.CharField(choices=[('AUCUN', 'AUCUN'), ('BIOLOGIE', 'BIOLOGIE'), ('RADIOLOGIE', 'RADIOLOGIE')], default='BIOLOGIE', max_length=25, verbose_name='DERNIERS EXAMENS DES DERNIERS MOIS')),
                ('details', models.TextField(blank=True, help_text='Préciser les details de la dernieres Consultation SVP', null=True)),
                ('diagnostique', models.TextField(blank=True, help_text='Diagnostique Finale', null=True)),
                ('time_zone', timezone_field.fields.TimeZoneField(default='UTC')),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rdv_patient', to='patients.patient')),
                ('symptome_adulte', models.ManyToManyField(blank=True, to='parametres.Adulte')),
                ('symptome_enfant', models.ManyToManyField(blank=True, to='parametres.Enfant')),
            ],
            options={
                'verbose_name': 'rdv',
                'verbose_name_plural': 'RDVS',
                'unique_together': {('patient', 'date_rdv')},
            },
        ),
    ]