from django.forms import forms, ModelForm, DateInput, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField, TextInput, DateTimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.forms import ModelForm, widgets
from django import forms
# from django.db.models import DateTimeField, CharField

import phonenumbers
from phonenumbers import NumberParseException
from parametres.forms import BootstrapInput

# from mon_ghs.MinimalSplitDateTimeMultiWidget import MinimalSplitDateTimeMultiWidget
# from mon_ghs.widgets import BootstrapDateTimePickerInput
from parametres.models import Enfant, Adulte, Abonnement
from .models import Patient, Rdv, Payment


class PatientForm(ModelForm):
    dob = DateTimeInput(attrs={
        'class': 'form-control dateimepicker',
    })
    class Meta:
        model=Patient
        fields=[
            'genre',
            'dob',
            'pays',
            'telephone1',
        ]

class PatientEditForm(ModelForm):
    dob = DateTimeInput(attrs={
        'class': 'form-control dateimepicker',
    })
    class Meta:
        model=Patient
        fields=[
            'genre',
            'dob',
            'poids',
            'groupe_sanguin',
            'telephone1',
            'telephone2',
            'adresse',
            'image',
            'details',
        ]

class PaymentForm(ModelForm):
    # patient=ModelChoiceField(queryset=Patient.objects.all(),empty_label="Patient", to_field_name="user_id")
    abonnement = ModelChoiceField(queryset=Abonnement.objects.all(), empty_label="Abonnement")
    class Meta:
        model= Payment
        fields = [
            'abonnement',
        ]

class rdvForm(ModelForm):
    class Meta:
        model=Rdv
        fields=[
            'date_rdv',
            'heure_rdv',
        ]

class rdvAutruiForm(ModelForm):
    class Meta:
        model=Rdv
        fields=[
            'nom',
            'prenoms',
            'date_naissance',
            'date_rdv',
            'heure_rdv',
        ]
        widgets = {
            # 'symptome_enfant': forms.CheckboxSelectMultiple(),
            'date_naissance': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y'),
        }

    def __init__(self, *args, **kwargs):
            super(rdvAutruiForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})

class SymptomeEnfantForm(ModelForm):
    # symptomes = CheckboxSelectMultiple()#forms.CheckboxSelectMultiple()
    # details = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
    class Meta:
        model=Rdv
        fields=[
            'symptome_enfant',
            # 'details'
        ]
        widgets = {
            'symptome_enfant': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(SymptomeEnfantForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class SymptomeAdulteForm(ModelForm):
    # symptomes = CheckboxSelectMultiple()#forms.CheckboxSelectMultiple()
    # details = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
    class Meta:
        model=Rdv
        fields=[
            'symptome_adulte',
            # 'details'
        ]
        widgets = {
            'symptome_adulte': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(SymptomeAdulteForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class EditRdvEnfantForm(forms.Form):
    symptome_enfant = forms.ModelMultipleChoiceField(queryset=Enfant.objects.all())
    # patient=ModelChoiceField(queryset=Patient.objects.all(),empty_label="Patient", to_field_name="user_id")
    #symptomes = ModelMultipleChoiceField(queryset=Symptome.objects.all(), widget=CheckboxSelectMultiple)
    # date_rdv = DateInput()
    class Meta:
        model=Rdv
        widgets = {
            'symptome_enfant': forms.CheckboxSelectMultiple(),
            'date_rdv': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%YT%H:%M'),
        }
        fields=[
            'date_rdv',
            'poids',
            'symptomes',
            'details'
        ]

    def __init__(self, *args, **kwargs):
        super(EditRdvEnfantForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    # def __init__(self, *args, **kwargs):
    #     super(EditRdvForm, self).__init__(*args, **kwargs)
    #     # input_formats to parse HTML5 datetime-local input to datetime field
    #     self.fields['date_rdv'].input_formats = ('%d/%m/%YT%H:%M',)

class EditRdvAdulteForm(forms.Form):
    symptome_adulte = forms.ModelMultipleChoiceField(queryset=Adulte.objects.all())
    # patient=ModelChoiceField(queryset=Patient.objects.all(),empty_label="Patient", to_field_name="user_id")
    #symptomes = ModelMultipleChoiceField(queryset=Symptome.objects.all(), widget=CheckboxSelectMultiple)
    # date_rdv = DateInput()
    class Meta:
        model=Rdv
        widgets = {
            'symptome_adulte': forms.CheckboxSelectMultiple(),
            'date_rdv': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%YT%H:%M'),
        }
        fields=[
            'date_rdv',
            'poids',
            'symptomes',
            'details'
        ]

    def __init__(self, *args, **kwargs):
        super(EditRdvAdulteForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    # def __init__(self, *args, **kwargs):
    #     super(EditRdvForm, self).__init__(*args, **kwargs)
    #     # input_formats to parse HTML5 datetime-local input to datetime field
    #     self.fields['date_rdv'].input_formats = ('%d/%m/%YT%H:%M',)

class BootstrapSelect(forms.Select):
    def __init__(self, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapSelect, self).__init__(attrs={
            'class': 'form-control input-sm',
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

        return '''<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapSelect, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)

class VerificationForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.HiddenInput())
    via = forms.ChoiceField(
        choices=[('sms', 'SMS'), ('call', 'APPEL')],
        widget=BootstrapSelect(size=3))

    def clean(self):
        data = self.cleaned_data
        phone_number = data['phone_number']
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Le Numéro Saisi est Incorrect')
        except NumberParseException as e:
            self.add_error('phone_number', e)

class TokenForm(forms.Form):
    token = forms.CharField(
        widget=BootstrapInput('Verification Token', size=6))