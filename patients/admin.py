from django.contrib import admin

from .models import Patient, Rdv, Payment
class PatientAdmin(admin.ModelAdmin):
    list_display = ['numero_patient', '__str__',  'telephone1', 'pays', 'dob', 'thumb']
    list_filter = ['pays', ]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'abonnement', 'prix', 'nb_consultation', 'is_abonne']
    list_filter = ['abonnement', ]

admin.site.register(Patient, PatientAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Rdv)

# Register your models here.
