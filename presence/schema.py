import graphene
from graphene_django.types import DjangoObjectType

from .models import Individu, Etudiant

# Type definition


class IndividuType(DjangoObjectType):
    class Meta:
        model = Individu


class EtudiantType(DjangoObjectType):
    class Meta:
        model = Etudiant

# Query definition


class Query(graphene.ObjectType):
    individus = graphene.List(IndividuType)

    def resolve_individus(self, info):
        return Individu.objects.all()
