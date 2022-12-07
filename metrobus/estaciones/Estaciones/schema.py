from graphene_django import DjangoObjectType
from graphene import relay


from estaciones.Estaciones.models import Estacion

class EstacionType(DjangoObjectType):
    class Meta:
        model = Estacion
