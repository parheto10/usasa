from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Abonnement, Hopital, Service, Faq, Pays, Adulte, Enfant
# class DetailSymptomeAdmin(admin.TabularInline):
#     model = DetailSymptome
#     extra = 0

class AdulteAdmin(ImportExportModelAdmin):
    list_display = ['id', 'symptome']

class EnfantAdmin(ImportExportModelAdmin):
    list_display = ['id', 'symptome']

class FaqAdmin(admin.ModelAdmin):
    list_display = ['question']
    list_display_links = ["question", ]
    prepopulated_fields = {'slug': ('question',)}

class AbonnementAdmin(admin.ModelAdmin):
    list_display = ['id', 'libelle', 'consultation', 'prix', 'status']
    list_editable = ['libelle', 'prix', 'consultation', 'status']

# class SymptomeAdmin(admin.ModelAdmin):
#    fields = ("categorie", 'symptome')
#    list_display = ('symptome', "categorie")
#    list_display_links = ('symptome',)
#    list_filter = ["categorie__nom", ]
#    # readonly_fields = ["plant_total"]
#    inlines = [DetailSymptomeAdmin]

admin.site.register(Adulte, AdulteAdmin)
admin.site.register(Enfant, EnfantAdmin)
admin.site.register(Abonnement, AbonnementAdmin)
admin.site.register(Pays)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Hopital)
# admin.site.register(CategorieSymptome)
# admin.site.register(DetailSymptome)
admin.site.register(Service)
# admin.site.register(Symptome, SymptomeAdmin)

# Register your models here.
