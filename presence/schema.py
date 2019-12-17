import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload

from .models import Individu, Etudiant, Categorie, Responsable, GroupeParticipant, Matiere

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

# Query definition


class Query(graphene.ObjectType):
    individus = graphene.List(IndividuType)
    categories = graphene.List(CategorieType)
    groupeParticipants = graphene.List(GroupeParticipantType)
    matieres = graphene.List(MatiereType)

    def resolve_individus(self, info):
        return Individu.objects.all()

    def resolve_categories(self, info):
        return Categorie.objects.all()

    def resolve_groupeParticipants(self, info):
        return GroupeParticipant.objects.all()

    def resolve_matieres(self, info):
        return Matiere.objects.all()

# Mutation definition


class CompareImage(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        file = Upload(required=True)

    def mutate(self, info, file):
        print(file)
        return CompareImage(success=True)


class Mutation(graphene.ObjectType):
    compare_image = CompareImage.Field()
