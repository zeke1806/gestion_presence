import graphene
from graphene_django.types import DjangoObjectType

from .models import Individu, Etudiant, Categorie

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

# Query definition


class Query(graphene.ObjectType):
    individus = graphene.List(IndividuType)
    categories = graphene.List(CategorieType)

    def resolve_individus(self, info):
        return Individu.objects.all()

    def resolve_categories(self, info):
        return Categorie.objects.all()
