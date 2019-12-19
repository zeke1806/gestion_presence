from django.contrib import admin

from .models import Individu, Responsable, Etudiant, GroupeParticipant, Appartenir, Categorie, Matiere, Evenement

# Register your models here.


class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('individu', 'num_matricule', 'niveau', 'parcours')


class EvenementAdmin(admin.ModelAdmin):
    list_display = ('categorie', 'matiere')


class IndividuAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'face_id')


admin.site.register(Individu, IndividuAdmin)
admin.site.register(Responsable)
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(GroupeParticipant)
admin.site.register(Appartenir)
admin.site.register(Categorie)
admin.site.register(Matiere)
admin.site.register(Evenement, EvenementAdmin)
