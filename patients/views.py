#from datetime import date
import requests
from dateutil import relativedelta
import time
import datetime
from datetime import datetime, date
from datetime import timedelta
import calendar
import dateutil

import os
import stripe
from parametres import twilio_params

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic
from twilio.rest import Client

from parametres.models import Adulte, Enfant, Abonnement
from .forms import PatientForm, rdvForm, PaymentForm, EditRdvAdulteForm, EditRdvEnfantForm, PatientEditForm, \
    SymptomeEnfantForm, SymptomeAdulteForm, rdvAutruiForm
from ghs_med.forms import UserForm
from .models import Patient, Rdv, Payment
from .utils import Calendar

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(generic.ListView):
    model = Rdv
    template_name = 'patients/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def calendrier(request):
    # patient = Patient.objects.get(user_id=request.user.id)
    # rdvs = Rdv.objects.all().filter(patient=patient)
    return render(request, 'patients/calendar.html', {})


def is_patient(user):
    return user.groups.filter(name='PATIENTS').exists()

def p_dashboard(request):
    patient = Patient.objects.all().filter(user_id=request.user.id)
    if patient:
        return redirect('/')
    else:
        return render(request, '/')

# @login_required(login_url='connexion')
def edit_patient(request, id=None):
    user = Patient.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Patient, id=id)
    form = PatientEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_id = user.id
        instance.save()
        # instance.save()
        messages.success(request, "Modification Effectuée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:pepinieres'))

    context = {
        "user":user,
        "instance": instance,
        "form": form,
    }
    return render(request, "patients/edit_dashboard.html", context)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def patient_dashboard(request):
    patient = Patient.objects.get(user_id=request.user.id)
    rdvs=Rdv.objects.all().filter(patient=patient).order_by('date_rdv')
    today = datetime.now()
    age = today.year - patient.dob.year
    context={
    'patient':patient,
    'rdvs': rdvs,
    'age': age,
    }
    return render(request,'patients/patient-dashboard.html',context=context)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def patient_rdvs(request):
    patient = Patient.objects.get(user_id=request.user.id)
    rdvs_OK=Rdv.objects.all().filter(patient=patient, is_ok=True).order_by('date_rdv')
    rdvs=Rdv.objects.all().filter(patient=patient, is_ok=False).order_by('date_rdv')
    # today = datetime.now()
    # age = today.year - patient.dob.year
    context={
    'patient':patient,
    'rdvs': rdvs,
    'rdvs_OK': rdvs_OK,
    # 'age': age,
    }
    return render(request,'patients/patient-rdvs.html',context=context)

def add_patient(request):
    userForm=UserForm()
    patientForm=PatientForm()
    if request.method=='POST':
        userForm=UserForm(request.POST)
        patientForm=PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            password = userForm.cleaned_data.get('password')
            email = userForm.cleaned_data.get('email')
            user.set_password(password)
            user.save()
            patient=patientForm.save(commit=False)
            numero = patient.numero_patient
            patient.user=user
            code_pays = (patient.pays.code).upper()
            if patient.pays.code == 'GHS-CIV':
                # tot = Rdv.objects.count()
                numero = str(Patient.objects.filter(pays__code="CIV").count() + 1)
                # madate = datetime.date.today()
                patient.numero_patient = "%s-00%s" % (code_pays, numero)
            elif patient.pays.code == 'GHS-CAM':
                # tot = Rdv.objects.count()
                numero = str(Patient.objects.filter(pays__code="CAM").count() + 1)
                # madate = datetime.date.today()
                patient.numero_patient = "%s-00%s" % (code_pays, numero)
            else:
                pass
            # sender = "+225-4-856-6846"
            # account_sid = 'AC7538f3cd9e32c282bfe2794c300d3a1b'
            account_sid = 'ACa9b3a79bcacc0ec38c29135fc5e395d1'
            # auth_token = 'a203471476d1f63807e60883fee01140'
            auth_token = '85aa55fb1024bfe53a8d05104af76b91'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                # messaging_service_sid='MG46bede6f533c252fa1e9843bde7f74aa',
                messaging_service_sid='MG2305ac0396286fee0017fff8db4c9a03',
                # body='bienvenus sur GHS',
                body='Compte créé avec Succès, Bienvenue Sur USASA-HEALTH - GHS, Votre code est %s' %(patient.pk),
                to=patient.telephone1
            )
            print(message.sid)
            # sender = "+225-4-856-6846"
            # sms = 'Compte créé avec Succès, Bienvenue Sur GLOBAL HEALTH SANTE - GHS, votre numero Patinet est : %s', (patient.numero_patient)
            # client = Client("AC6f9cb34825cbcf101f780c6094364588", "5f8cbe6a6c2c683e7d98d4d336b02900")
            # client.messages.create(
            #     to=["+225%s"%patient.telephone1, sender],
            #     from_= sender,
            #     body=sms
            # )
            # sender = "+225-4-856-6846"
            # sms = 'Compte créé avec Succès, Bienvenue Sur GLOBAL HEALTH SANTE - GHS, votre numero Patinet est : %s', (patient.numero_patient)
            # client = Client("AC6f9cb34825cbcf101f780c6094364588", "5f8cbe6a6c2c683e7d98d4d336b02900")
            # client.messages.create(
            #                        to=["+225%s"%patient.telephone1],
            #                        from_=sender,
            #                        body=sms)
            patient=patient.save()
            # subject = 'Bienvenue Sur GLOBAL HEALTH SANTE - GHS'
            # message = 'Compte créé avec Succès, Bienvenue Sur GLOBAL HEALTH SANTE - GHS, votre numero Patinet est : %s', (patient.numero_patient),
            # send_mail(
            #     subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [email],
            #     fail_silently=False,
            # )
            print(patient)
            patient_group = Group.objects.get_or_create(name='PATIENTS')
            patient_group[0].user_set.add(user)
            patient = authenticate(username=user.username, password=password)
            dj_login(request, patient)
            # if next:
            #     return redirect(next)
            messages.success(request, "Inscription effectuée avec succès")
            return HttpResponseRedirect(reverse('patient:rdv'))
        else:
            messages.error(request, "Désole Une Erreur est Survenue, Réessayer SVP !!!")

    context = {
        'userForm': userForm,
        'patientForm': patientForm
    }
    return render(request,'patients/add_patient.html',context=context)

# def checkout(request):
#     patient = Patient.objects.get(user_id=request.user.id)
#     context = {
#         'patient': patient,
#     }
#     return render(request, 'patients/paiement.html', context)
@login_required(login_url='connexion')
@user_passes_test(is_patient)
def rdv_patient(request):
    # patient = request.user.patient
    patient = Patient.objects.get(user_id=request.user.id)
    form=rdvForm()
    # patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    if request.method=='POST':
        form=rdvForm(request.POST)
        if form.is_valid():
            rdv=form.save(commit=False)
            rdv.patient = patient
            account_sid = 'ACa9b3a79bcacc0ec38c29135fc5e395d1'
            auth_token = '85aa55fb1024bfe53a8d05104af76b91'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                messaging_service_sid='MG2305ac0396286fee0017fff8db4c9a03',
                body='Rendz-vous Validé avec Succès à la date du %s à %s :' %(rdv.date_rdv, rdv.heure_rdv),
                to=patient.telephone1
            )
            print(message.sid)
            # rdv.patient=Patient.objects.get(user_id=request.user.id)
            rdv.save()
            # form.save_m2m()
        return HttpResponseRedirect(reverse('patient:init_rdv'))
    mydict = {'form': form, 'patient': patient}
    return render(request,'patients/calendar1.html',context=mydict)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def rdv_autrui(request):
    patient = request.user.patient
    form = rdvAutruiForm()
    if request.method == 'POST':
        form = rdvAutruiForm(request.POST)
        if form.is_valid():
            rdv_autrui = form.save(commit=False)
            rdv_autrui.patient = patient
            today = date.today()
            rdv_autrui.age = today.year - (rdv_autrui.date_naissance).year
            rdv_autrui.save()
            if rdv_autrui.age <=16:
                return HttpResponseRedirect(reverse('patient:symptomes_enfants'))
            elif rdv_autrui.age > 16 :
                return HttpResponseRedirect(reverse('patient:symptomes_adultes'))
        # return HttpResponseRedirect(reverse('patient:dashboard'))
    mydict = {'form': form, 'patient': patient}
    return render(request, 'patients/autruiForm.html', context=mydict)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def symptomes_adultes(request):
    patient = request.user.patient
    form=SymptomeAdulteForm()
    # patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    if request.method=='POST':
        form=rdvForm(request.POST)
        if form.is_valid():
            symptome=form.save(commit=False)
            symptome.patient = patient
            symptome.save()
            # symptome.save_m2m()
        return HttpResponseRedirect(reverse('patient:dashboard'))
    mydict = {'form': form, 'patient': patient}
    return render(request,'patients/symptomesForm.html',context=mydict)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def symptomes_enfants(request):
    patient = request.user.patient
    form=SymptomeEnfantForm()
    # patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    if request.method=='POST':
        form=rdvForm(request.POST)
        if form.is_valid():
            symptome=form.save(commit=False)
            symptome.patient = patient
            symptome.save()
            # symptome.save_m2m()
        return HttpResponseRedirect(reverse('patient:dashboard'))
    mydict = {'form': form, 'patient': patient}
    return render(request,'patients/symptomesForm.html',context=mydict)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def init_rdv(request):
    return render(request,'patients/rdv_init.html')

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def rdv_ok(request):
    return render(request,'patients/rdv_oh.html')

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def edit_rdv_adulte(request, id=None):
    user = request.user.patient
    instance = get_object_or_404(Rdv, id=id)
    form = EditRdvAdulteForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.patient = user
        instance.save()
        messages.success(request, "RDV Modifié avec succès")
        return HttpResponseRedirect(reverse('patient:dashboard'))
    context = {
        "instance": instance,
        "form":form
    }
    return render(request, "patients/rdv_edit.html", context)


@login_required(login_url='connexion')
@user_passes_test(is_patient)
def edit_rdv_enfant(request, id=None):
    user = request.user.patient
    instance = get_object_or_404(Rdv, id=id)
    form = EditRdvEnfantForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.patient = user
        instance.save()
        messages.success(request, "RDV Modifié avec succès")
        return HttpResponseRedirect(reverse('patient:dashboard'))
    context = {
        "instance": instance,
        "form":form
    }
    return render(request, "patients/rdv_edit.html", context)


@login_required(login_url='connexion')
@user_passes_test(is_patient)
def detail_rdv(request, id=None):
    user = request.user.patient
    instance = get_object_or_404(Rdv, id=id)
    context = {
        "instance": instance,
    }
    return render(request, "patients/detail_rdv.html", context)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def abonnement(request):
    paymentForm = PaymentForm()
    patient=Patient.objects.get(user_id=request.user.id)
    abonnements = Abonnement.objects.all()
    if request.method=='POST':
        paymentForm=PaymentForm(request.POST)
        if paymentForm.is_valid():
            payment=paymentForm.save(commit=False)
            payment.patient = Patient.objects.get(user_id=request.user.id)
            payment.patient.is_abonne = True
            payment.patient.nb_consultation = payment.abonnement.consultation
            payment.save()
        return HttpResponseRedirect(reverse('patient:rdv'))
    mydict = {
        'paymentForm': paymentForm,
        'patient': patient,
        'abbonements':abonnements
    }
    return render(request,'patients/paiement1.html',context=mydict)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def checkout(request, id=None):
    patient = request.user.patient
    abonnement = Abonnement.objects.get(pk=id)
    mydict = {
        'patient': patient,
        'abonnement': abonnement,
    }
    return render(request,'patients/checkout.html',context=mydict)

stripe.api_key = "sk_test_haCEhsbVDs1nrfDohimNM12j"
def checkout_session(request, id=None):
    abonnement = Abonnement.objects.get(pk=id)
    session = stripe.checkout.Session.create(
        #definir le mode paiement carte
        payment_method_types = ['card'],
        line_items=[{
            'price_data': {
                'currency': 'xof',
                'product_data': {
                    'name': abonnement.libelle,
                },
                # 'unit_amount': float(abonnement.prix)*100,
                'unit_amount': abonnement.prix,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/patients/paiement_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/patients/paiement_error',
        client_reference_id = id
    )
    return redirect(session.url, code=303)


def paiement_success(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    id = session.client_reference_id  #Abonnement.objects.get(pk=id)
    abonnement = Abonnement.objects.get(pk=id)
    patient = request.user.patient
    Num = patient.numero_patient
    nb_consultation = abonnement.consultation
    Payment.objects.create(
        patient=patient,
        abonnement=abonnement,
        prix=abonnement.prix,
        nb_consultation=abonnement.consultation,
        is_abonne=True
    )
    context = {
        'Num': Num,
        'nb_consultation': nb_consultation,

    }
    return render(request, 'success.html', context)

def paiement_error(request):
    return render(request, 'cancel.html')

def send_sms(request):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    if "username" in request.POST and "sendto" in request.POST and "message" in request.POST:
        username = request.POST["username"]
        sendto = request.POST["sendto"]
        message=request.POST["message"]
        client.messages.create(to=sendto,
                               from_=settings.TWILIO_NUMBER,
                               body=message)
        return HttpResponse("Send")
    return render(request, 'drinks/send_sms.html', {'send_sms': send_sms})


from django.shortcuts import render, redirect

from .forms import VerificationForm, TokenForm

account_sid = 'ACa9b3a79bcacc0ec38c29135fc5e395d1'
auth_token = '85aa55fb1024bfe53a8d05104af76b91'
# verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])
client = Client(account_sid, auth_token)

def verifications(phone_number, via):
    return client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(to=phone_number, channel=via)

def verification_checks(phone_number, token):
    return client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verification_checks.create(to=phone_number, code=token)

def phone_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            request.session['phone_number'] = form.cleaned_data['phone_number']
            verification = twilio_params.verifications(form.cleaned_data['phone_number'], form.cleaned_data['via'])
            return redirect('patient:token_validation')
    else:
        form = VerificationForm()
    return render(request, 'patients/phone_verification.html', {'form': form})


def token_validation(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = twilio_params.verification_checks(request.session['phone_number'], form.cleaned_data['token'])

            if verification.status == 'approved':
                request.session['is_verified'] = True
                return redirect('patient:inscription')
            else:
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, 'patients/token_validation.html', {'form': form})


def verified(request):
    if not request.session.get('is_verified'):
        return redirect('patient:inscription')
    return render(request, 'patients/add_patient.html')
