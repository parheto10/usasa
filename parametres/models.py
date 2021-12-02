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

from django.urls import reverse
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from sorl.thumbnail import get_thumbnail

def upload_logo_site(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "logos/" + self.code + ".jpeg"

ALERT_SYMPTOMES = (
    ('ALERTE', 'ALERTE'),
    ('NORMAL', 'NORMAL'),
)

class Pays(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    code = models.CharField(max_length=3, verbose_name="CODE PAYS")
    libelle = models.CharField(max_length=255, verbose_name="NOM PAYS")

    def __str__(self):
        return '%s (%s)' %(self.libelle, self.code)

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper()
        self.libelle = self.libelle.upper()
        super(Pays, self).save(force_insert, force_update)

    class Meta:
        # ordering = ['symptome']
        verbose_name_plural = "PAYS"
        verbose_name = "pays"

class Abonnement(models.Model):
    libelle = models.CharField(max_length=255)
    consultation = models.PositiveIntegerField(default=0, verbose_name="NOMBRE DE CONSULTATION")
    prix = models.PositiveIntegerField(default=2500)
    status = models.BooleanField(default=False, null=True)
    details = models.TextField()

    def __str__(self):
        return "%s - %s" %(self.libelle, self.prix)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        # self.pays = self.pays.upper()
        super(Abonnement, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "ABONNEMENTS"
        verbose_name = "abonnement"

class Adulte(models.Model):
    symptome = models.CharField(max_length=500, verbose_name="SYMPTOME")

    def __str__(self):
        return '%s' %(self.symptome)

    def save(self, force_insert=False, force_update=False):
        self.symptome = self.symptome.upper()
        super(Adulte, self).save(force_insert, force_update)

    class Meta:
        ordering = ['symptome']
        verbose_name_plural = "SYMPTOMES ADULTES"
        verbose_name = "symptome adulte"

class Nourrison(models.Model):
    symptome = models.CharField(max_length=500, verbose_name="SYMPTOME")
    signal = models.CharField(max_length=50, choices=ALERT_SYMPTOMES, default="NORMAL")

    def __str__(self):
        return '%s' %(self.symptome)

    def save(self, force_insert=False, force_update=False):
        self.symptome = self.symptome.upper()
        super(Nourrison, self).save(force_insert, force_update)

    class Meta:
        ordering = ['symptome']
        verbose_name_plural = "SYMPTOMES NOURRISSONS"
        verbose_name = "symptome nourrisson et enfant"

class Enfant(models.Model):
    symptome = models.CharField(max_length=500, verbose_name="SYMPTOME")
    signal = models.CharField(max_length=50, choices=ALERT_SYMPTOMES, default="NORMAL")

    def __str__(self):
        return '%s' %(self.symptome)

    def save(self, force_insert=False, force_update=False):
        self.symptome = self.symptome.upper()
        super(Enfant, self).save(force_insert, force_update)

    class Meta:
        ordering = ['symptome']
        verbose_name_plural = "SYMPTOMES ENFANTS ET ADOLESCENTS"
        verbose_name = "symptome enfant adolescent"


class Hopital(models.Model):
    code = models.CharField(max_length=5, verbose_name="CODE", unique=True)
    libelle = models.CharField(max_length=250, verbose_name="NOM")
    pays = CountryField(blank_label='(Préciser Le Pays)')
    ville = models.CharField(max_length=250, verbose_name="VILLE")
    adresse = models.CharField(max_length=250, verbose_name="ADRESSE", blank=True)
    telephone1 = PhoneNumberField(help_text="+22545485648")  # CharField(max_length=50, verbose_name="TELEPHONE 1")
    telephone2 = PhoneNumberField(help_text="+22545485648", blank=True)
    faxe = models.CharField(max_length=50, verbose_name="FAXE", blank=True)
    email = models.EmailField(max_length=120, blank=True, verbose_name="ADRESSE EMAIL")
    siteweb = models.CharField(max_length=120, blank=True, verbose_name="SITE WEB")
    logo = models.ImageField(verbose_name="Logo", upload_to=upload_logo_site, blank=True)
    image1 = models.ImageField(verbose_name="Image 1", upload_to=upload_logo_site, blank=True)
    image2 = models.ImageField(verbose_name="Image 2", upload_to=upload_logo_site, blank=True)
    # image3 = models.ImageField(verbose_name="Image 3", upload_to=upload_logo_site, blank=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s - %s : %s' % (self.libelle, self.telephone1, self.adresse)

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper()
        self.ville = self.ville.upper()
        self.libelle = self.libelle.upper()
        self.adresse = self.adresse.upper()
        # self.pays = self.pays.upper()
        super(Hopital, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "HOPITAUX"
        verbose_name = "hopital"

    def Logo(self):
        if self.logo:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.logo.url)
        else:
            return "Aucun Logo"

    Logo.short_description = 'Logo'

class Service(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    details = models.TextField()
    image = models.ImageField(upload_to="%Y%m", blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.nom

    def save(self, force_insert=False, force_update=False):
        self.nom = self.nom.upper()
        super(Service, self).save(force_insert, force_update)

    def Image(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return "Aucune image"

    Image.short_description = 'Image'

    class Meta:
        verbose_name_plural = "SERVICES"
        verbose_name = "service"

class Faq(models.Model):
    question = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    reponses = models.TextField(blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "FAQS"
        verbose_name = "faq"