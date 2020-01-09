from django.contrib import admin

from .models import Individu, Responsable, Etudiant, GroupeParticipant, Appartenir, Categorie, Matiere, Evenement

# Register your models here.


class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('id', 'individu', 'num_matricule', 'niveau', 'parcours')


class EvenementAdmin(admin.ModelAdmin):
    list_display = ('id', 'categorie', 'matiere')


class IndividuAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'face_id')


class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_categorie')


class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('id', 'individu')


class MatiereAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_matiere')


class GroupeParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_groupe_participant')


admin.site.register(Individu, IndividuAdmin)
admin.site.register(Responsable, ResponsableAdmin)
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(GroupeParticipant, GroupeParticipantAdmin)
admin.site.register(Appartenir)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Evenement, EvenementAdmin)
