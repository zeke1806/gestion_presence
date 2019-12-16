import graphene
from graphene_django.types import DjangoObjectType

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
    groupeParticipants =graphene.List(GroupeParticipantType)
    matieres = graphene.List(MatiereType)

    def resolve_individus(self, info):
        return Individu.objects.all()

    def resolve_categories(self, info):
        return Categorie.objects.all()

    def resolve_groupeParticipants(self, info):
        return GroupeParticipant.objects.all()

    def resolve_matieres(self, info):
        return Matiere.objects.all()
