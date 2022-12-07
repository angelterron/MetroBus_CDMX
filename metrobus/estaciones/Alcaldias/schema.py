from graphene_django import DjangoObjectType

from estaciones.Alcaldias.models import Alcaldia


class AlcaldiaType(DjangoObjectType):
    class Meta:
        model = Alcaldia