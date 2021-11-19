# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid

from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.db import models
import datetime
import time
import arrow
from timezone_field import TimeZoneField

from django.urls import reverse
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from sorl.thumbnail import get_thumbnail

from parametres.models import Adulte, Enfant, Service, Abonnement, Pays


def upload_images(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "images/" + ".jpeg"

def images_assure(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "assure/" + ".jpeg"

GENRE = (
        ('H', 'HOMMME'),
        ('F', 'FEMME'),
    )

EXAMENS = (
    ("AUCUN", "AUCUN"),
    ("BIOLOGIE", "BIOLOGIE"),
    ("RADIOLOGIE", "RADIOLOGIE"),
)

ALERTS = (
    ("APPEL", "APPEL"),
    ("EMAIL", "EMAIL"),
    ("SMS", "SMS"),
)

GROUPE_SANGUIN = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'A-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)

class Patient(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_patient = models.CharField(max_length=15, verbose_name="NUMERO", unique=True, blank=True, null=True)
    genre = models.CharField(max_length=10, verbose_name="GENRE", choices=GENRE, default="H", blank=True, null=True)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, blank=True, null=True)  # CountryField(blank=True, null=True)
    dob = models.DateField(verbose_name="Date de Naissance")
    poids = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    groupe_sanguin = models.CharField(max_length=3, verbose_name="GROUPE SANGUIN", choices=GROUPE_SANGUIN, default="A+", blank=True, null=True)
    telephone1 = models.CharField(max_length=50, verbose_name="TELEPHONE 1", help_text="Veuillez entrer un Numero Au format International Exple: +225 xx xx xx xx xx")
    telephone2 = models.CharField(max_length=50, verbose_name="TELEPHONE 2", blank=True, null=True)
    adresse = models.CharField(max_length=255, verbose_name="ADRESSE", blank=True, null=True)
    image = models.ImageField(upload_to="upload_image", blank=True, null=True)
    details = models.TextField(verbose_name="Historique Médical", null=True, blank=True)
    nb_consultation = models.PositiveIntegerField(default=0, verbose_name="NOMBRE DE CONSULTATION")

    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "PATIENTS"
        verbose_name = "patient"
        ordering = ["-add_le"]

    def Patient(self):
        return '%s %s' %(self.user.last_name, self.user.first_name)

    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        if self.user.last_name or self.user.first_name:
            return '%s %s' %(self.user.last_name, self.user.first_name)
        else:
            return self.user.username

    def thumb(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return "Aucune photo"
    thumb.short_description = 'Image'

    # def save(self, force_insert=False, force_update=False):
    #     code_pays = (self.pays.code).upper()
    #     last_id = 1
    #     if self.pays.code == 'GHS-CIV':
    #         # tot = Rdv.objects.count()
    #         numero = str(Patient.objects.filter(pays__code="CIV").count() + 1)
    #         # madate = datetime.date.today()
    #         self.numero_patient = "%s-00%s" % (code_pays, numero)
    #     elif self.pays.code == 'GHS-CAM':
    #         # tot = Rdv.objects.count()
    #         numero = str(Patient.objects.filter(pays__code="CAM").count() + 1)
    #         # madate = datetime.date.today()
    #         self.numero_patient = "%s-00%s" % (code_pays, numero)
    #     else:
    #         pass
    #     # # if not self.id:
    #     # code_pays = (self.pays.code).upper()
    #     # last_id = 1
    #     # if self.pays.code == 'CI':
    #     #     # last_id = 1
    #     #     tot = Profile.objects.filter(pays__code="CIV").count()
    #     #     # last_id = 1
    #     #     numero = str(tot + last_id)
    #     #     # madate = datetime.date.today()
    #     #     self.numero_patient = code_pays + "-00%s" %(numero)
    #     # elif self.pays == 'CA':
    #     #     # last_id = 1
    #     #     tot = Profile.objects.filter(pays__code="CIV").count()
    #     #     numero = str(tot + last_id)
    #     #     # madate = datetime.date.today()
    #     #     self.numero_patient = code_pays + "-00%s" %(numero)
    #     # else:
    #     #     pass
    #     super(Patient, self).save(force_insert, force_update)

    def get_absolute_url(self):
        #return reverse('patient:dashboard', args=[self.id])
        return reverse("patient:profile", kwargs={"username": self.user.username})
        # return reverse('patient:dashboard', kwargs={"username":self.user.username}

class Payment(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='abonnement_patient')
    abonnement = models.ForeignKey(Abonnement, on_delete=models.CASCADE, related_name='abonnement_formule', default=1)
    prix = models.PositiveIntegerField(default=0, blank=True)
    nb_consultation = models.PositiveIntegerField(default=0, blank=True)
    is_abonne = models.BooleanField(default=False, verbose_name="ABONNEMENT")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # class Meta:
    #     unique_together = ['patient', 'abonnement']

    def __str__(self):
        return str(self.patient.user.username)

    # def save(self, force_insert=False, force_update=False):
    #     if self.abonnement and self.is_abonne == True:
    #         self.nb_consultation = self.abonnement.consultation
    #     super(Payment, self).save(force_insert, force_update)

class Rdv(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    code = models.CharField(max_length=150, blank=True, verbose_name='CODE RDV', help_text="LE CODE RDV EST GENERE AUTOMATIQUEMENT")
    date_rdv = models.DateField(verbose_name="DATE DU RDV")
    heure_rdv = models.TimeField(verbose_name="HEURE DU RDV")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rdv_patient')

    # RDV pour Autrui
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenoms = models.CharField(max_length=255, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(default=0, blank=True, null=True)

    poids = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    taille = models.PositiveIntegerField(default=0, verbose_name="Taille(cm)", blank=True)
    ta = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="TENSION ARTERIELLE(TA)", blank=True, null=True)
    poults = models.PositiveIntegerField(default=0)
    systolique = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)#models.PositiveIntegerField(default=0)
    diastolique = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)#models.PositiveIntegerField(default=0)
    symptome_enfant = models.ManyToManyField(Enfant, blank=True)
    symptome_adulte = models.ManyToManyField(Adulte, blank=True)
    nb_rdv = models.PositiveIntegerField(default=0)
    is_ok = models.BooleanField(default=False)
    alert = models.CharField(max_length=100, choices=ALERTS, default="EMAIL", verbose_name="ALERT RDVS")
    last_examen = models.CharField(max_length=25, choices=EXAMENS, verbose_name="DERNIERS EXAMENS DES DERNIERS MOIS", default="BIOLOGIE")
    details = models.TextField(help_text="Préciser les details de la dernieres Consultation SVP", blank=True, null=True)
    diagnostique = models.TextField(help_text="Diagnostique Finale", blank=True, null=True)
    time_zone = TimeZoneField(default='UTC')
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-add_le', '-update_le']

    def Patient(self):
        return '%s %s' % (self.patient.user.last_name, self.patient.user.first_name)

    def __str__(self):
        return 'Rdv de %s le %s' %(self.patient, self.date_rdv)


    def clean(self):
        # numerotation automatique
        if not self.id:
            tot = Rdv.objects.count()
            numero = tot + 1
            madate = datetime.date.today()
            self.code = "%s-%s" % (numero, datetime.date.strftime(madate, '%d/%m/%Y'))
            if self.diastolique and self.systolique:
                self.ta = (self.diastolique + self.systolique) / 2

    class Meta:
        verbose_name_plural = "RDVS"
        verbose_name = "rdv"
        # unique_together = ['patient', 'date_rdv']

    def get_symptomes(self):
        ret = ''
        if self.symptome_enfant:
            for symp in self.symptome_enfant.all():
                ret = ret + symp.symptome + ','
            return ret[:-1]
        elif self.symptome_adulte:
            for symp in self.symptome_adulte.all():
                ret = ret + symp.symptome + ','
            return ret[:-1]
        else:
            pass

    # def get_symptomes(self):
    #     ret = ''
    #     # print(self.projet.all())
    #     for symp in self.symptomes.all():
    #         ret = ret + symp.symptome + ','
    #     return ret[:-1]

    def get_absolute_url(self):
        return reverse('patient:rdv', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('patient:rdv')
        return f'<a href="{url}"> {self.code} </a>'


# class Test(models.Model):
#     user = models.CharField(max_length=255, verbose_name="Nom Utilisateur")
#     nom = models.CharField(max_length=255, verbose_name="Nom")
#     prenoms = models.CharField(max_length=255, verbose_name="Prénoms")