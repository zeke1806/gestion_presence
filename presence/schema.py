import graphene
import face_recognition
import base64
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from django.core.files.base import ContentFile
from django.utils import timezone

from .models import Individu, Etudiant, Categorie, Responsable, GroupeParticipant, Matiere, Evenement

# Type definition


class IndividuType(DjangoObjectType):
    class Meta:
        model = Individu


class EtudiantType(DjangoObjectType):
    class Meta:
        model = Etudiant


class CategorieType(DjangoObjectType):
    class Meta:
        model = Categorie


class ResponsableType(DjangoObjectType):
    class Meta:
        model = Responsable


class GroupeParticipantType(DjangoObjectType):
    class Meta:
        model = GroupeParticipant


class MatiereType(DjangoObjectType):
    class Meta:
        model = Matiere


class EvenementType(DjangoObjectType):
    class Meta:
        model = Evenement

# Query definition


class Query(graphene.ObjectType):
    individus = graphene.List(IndividuType)
    categories = graphene.List(CategorieType)
    groupeParticipants = graphene.List(GroupeParticipantType)
    matieres = graphene.List(MatiereType)
    responsables = graphene.List(ResponsableType)
    evenements = graphene.List(EvenementType)
    etudiants = graphene.List(EtudiantType)
    gp_members = graphene.List(
        EtudiantType, gp_id=graphene.ID(required=True))
    evenement = graphene.Field(EvenementType, idEvent=graphene.ID())

    def resolve_individus(self, info):
        return Individu.objects.all()

    def resolve_categories(self, info):
        return Categorie.objects.all()

    def resolve_groupeParticipants(self, info):
        return GroupeParticipant.objects.all()

    def resolve_matieres(self, info):
        return Matiere.objects.all()

    def resolve_responsables(self, info):
        return Responsable.objects.all()

    def resolve_evenements(self, info):
        return Evenement.objects.all()

    def resolve_etudiants(self, info):
        return Etudiant.objects.all()

    def resolve_gp_members(self, info, gp_id=None):
        gp = GroupeParticipant.objects.get(id=gp_id)
        return gp.membres.all()

    def resolve_evenement(self, info, idEvent):
        return Evenement.objects.get(id=idEvent)

# Mutation definition


class CompareImage(graphene.Mutation):
    """
        1) Reception d'une image en base 64
        2) Decoder l'image
        3) Encoder l'image avec face_recognition
        4) Recuperer la liste d'individus
        5) Creer une liste d'image des individus encoder avec face_recognition
        6) Comparer la liste d'image individus avec l'image recu
        7) Boucler sur le resultat
        8) Si une entree match, on me present a True, on break et on retourne present
    """
    present = graphene.Boolean()

    class Arguments:
        file = Upload(required=True)

    def mutate(self, info, file):
        present = False

        file_format, imgstr = file["uri"].split(';base64,')
        ext = file_format.split('/')[-1]
        to_compare = ContentFile(base64.b64decode(imgstr),
                                 name=file["name"] + "." + ext)
        to_compare_encode = face_recognition.face_encodings(
            face_recognition.load_image_file(to_compare))

        if to_compare_encode:
            to_compare_encode = to_compare_encode[0]
        else:
            raise Exception("Impossible de traiter l'image")

        individus_image_encode = []
        individus = Individu.objects.all()
        for individu in individus:
            encode_image = face_recognition.face_encodings(
                face_recognition.load_image_file(individu.face_id))[0]
            individus_image_encode.append(encode_image)

        results = face_recognition.compare_faces(
            individus_image_encode, to_compare_encode, tolerance=0.53)

        for result in results:
            if result:
                present = True
                break

        return CompareImage(present=present)


class CreateEvent(graphene.Mutation):
    evenement = graphene.Field(EvenementType)

    class Arguments:
        responsables = graphene.List(graphene.ID)
        presences = graphene.List(graphene.ID)
        groupe_participants = graphene.List(graphene.ID)
        categorie = graphene.ID()
        matiere = graphene.ID()
        date_debut = graphene.DateTime()
        date_fin = graphene.DateTime()

    def mutate(self, info, responsables=None, presences=None, groupe_participants=None, categorie=None, matiere=None, date_debut=None, date_fin=None):
        categorie = Categorie.objects.get(id=categorie)
        evenement = Evenement.objects.create(categorie=categorie)

        if matiere:
            matiere = Matiere.objects.get(id=matiere)
            evenement.matiere = matiere
        if responsables:
            for responsable in responsables:
                responsable = Responsable.objects.get(id=responsable)
                evenement.responsables.add(responsable)
        if presences:
            for etudiant in presences:
                etudiant = Etudiant.objects.get(id=etudiant)
                evenement.presences.add(etudiant)
        if groupe_participants:
            for groupe in groupe_participants:
                groupe = GroupeParticipant.objects.get(id=groupe)
                evenement.groupe_participants.add(groupe)
        if date_debut:
            evenement.date_debut = date_debut
        if date_fin:
            evenement.date_fin = date_fin

        evenement.save()
        return CreateEvent(evenement=evenement)


class SetEvent(graphene.Mutation):
    evenement = graphene.Field(EvenementType)

    class Arguments:
        id_event = graphene.ID(required=True)
        responsables = graphene.List(graphene.ID)
        presences = graphene.List(graphene.ID)
        groupe_participants = graphene.List(graphene.ID)
        categorie = graphene.ID()
        matiere = graphene.ID()
        date_debut = graphene.DateTime()
        date_fin = graphene.DateTime()
        cancel = graphene.Boolean()

    def mutate(self, info, id_event, responsables=None, presences=None, groupe_participants=None, categorie=None, matiere=None, date_debut=None, date_fin=None, cancel=None):
        # Pour les listes (principe de mutation)
        # On recoit une liste d'id d'entree
        # On supprime d'abord toute les entrees et on remplaces juste
        # Par la nouvelle liste
        evenement = Evenement.objects.get(id=id_event)

        if responsables:
            evenement.responsables.clear()
            for responsable in responsables:
                responsable = Responsable.objects.get(id=responsable)
                evenement.responsables.add(responsable)
        if presences:
            evenement.presences.clear()
            for etudiant in presences:
                etudiant = Etudiant.objects.get(id=etudiant)
                evenement.presences.add(etudiant)
        if groupe_participants:
            evenement.groupe_participants.clear()
            for groupe in groupe_participants:
                groupe = GroupeParticipant.objects.get(id=groupe)
                evenement.groupe_participants.add(groupe)
        if categorie:
            categorie = Categorie.objects.get(id=categorie)
            evenement.categorie = categorie
        if matiere:
            matiere = Matiere.objects.get(id=matiere)
            evenement.matiere = matiere
        if date_debut:
            evenement.date_debut = timezone.localtime(date_debut)
        if date_fin:
            evenement.date_fin = timezone.localtime(date_debut)
        if cancel:
            evenement.date_debut = None

        evenement.save()
        return SetEvent(evenement=evenement)


class Mutation(graphene.ObjectType):
    compare_image = CompareImage.Field()
    create_event = CreateEvent.Field()
    set_event = SetEvent.Field()
