from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from .views import (
    patient_dashboard,
    add_patient,
    rdv_patient,
    CalendarView,
    abonnement,
    edit_rdv_adulte,
    edit_rdv_enfant,
    detail_rdv,
    checkout,
    edit_patient, rdv_ok, symptomes_enfants, symptomes_adultes, patient_rdvs, checkout_session, paiement_success, paiement_error,
    phone_verification, token_validation, verified, init_rdv, rdv_autrui
    # profile_patient,
    # profile_setting

)

app_name= 'patient'

urlpatterns = [
    # Patient
    path('dashboard/', patient_dashboard, name='dashboard'),
    path('init_rdv/', init_rdv, name='init_rdv'),
    path('patient_rdvs/', patient_rdvs, name='patient_rdvs'),
    path('abonnement/', abonnement, name='abonnement'),
    path('calendrier/', CalendarView.as_view(), name='calendrier'),
    # path('settings/', profile_setting, name='settings'),
    path('inscription/', add_patient, name="inscription"),
    path('edit_rdv/<int:id>', edit_rdv_adulte, name="edit_rdv_adulte"),
    path('edit_rdv/<int:id>', edit_rdv_enfant, name="edit_rdv_enfant"),
    path('detail_rdv/<int:id>', detail_rdv, name="detail_rdv"),
    path('rdv_autrui/', rdv_autrui, name="rdv_autrui"),
    path('rdv_ok/', rdv_ok, name="rdv_ok"),
    path('rdv/', rdv_patient, name="rdv"),
    path('rdv_symptomes_enfants/', symptomes_enfants, name="symptomes_enfants"),
    path('rdv_symptomes_adultes/', symptomes_adultes, name="symptomes_adultes"),
    path('edit_patient/<int:id>', edit_patient, name="edit_patient"),
    path('paiement/<int:id>', checkout, name="paiement"),
    path('checkout_session/<int:id>', checkout_session, name="checkout_session"),
    path('paiement_success/', paiement_success, name="paiement_success"),
    path('paiement_error/', paiement_error, name="paiement_error"),

    path('verification/', phone_verification, name='phone_verification'),  # noqa: E501
    path('verification/token/', token_validation, name='token_validation'),  # noqa: E501
    path('verified/', verified, name='verified'),

]