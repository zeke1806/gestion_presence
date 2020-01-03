import graphene
import face_recognition
import base64
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from django.core.files.base import ContentFile

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


class SetEvent(graphene.Mutation):
    event = graphene.Field(EvenementType)

    class Arguments:
        event_id = graphene.ID(required=False)
        responsables_id = graphene.List(graphene.ID, required=False)
        presences_id = graphene.List(graphene.ID, required=False)
        groupe_participants_id = graphene.List(graphene.ID, required=False)
        categorie_id = graphene.ID(required=False)
        matiere_id = graphene.ID(required=False)
        date_debut = graphene.Date(required=False)
        date_fin = graphene.Date(required=False)

    def mutate(self, info, event_id=None, responsables_id=None,
               presences_id=None, groupe_participants_id=None, categorie_id=None, matiere_id=None,
               date_debut=None, date_fin=None):
        if event_id:
            evenement = Evenement.objects.get(id=event_id)
        else:
            evenement = Evenement.objects.create()
        if responsables_id:
            for identifiant in responsables_id:
                evenement.responsables.add(
                    Responsable.objects.get(id=identifiant))
        if presences_id:
            for identifiant in presences_id:
                evenement.presences.add(Etudiant.objects.get(id=identifiant))
        if groupe_participants_id:
            for identifiant in groupe_participants_id:
                evenement.groupe_participants_id(
                    GroupeParticipant.objects.get(id=identifiant))
        if categorie_id:
            evenement.categorie = Categorie.objects.get(id=categorie_id)
        if matiere_id:
            evenement.matiere = Matiere.objects.get(id=matiere_id)
        if date_debut:
            evenement.date
        evenement.save()
        return SetEvent(event=evenement)


class Mutation(graphene.ObjectType):
    compare_image = CompareImage.Field()
    set_event = SetEvent.Field()
