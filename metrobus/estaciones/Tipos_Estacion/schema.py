from graphene_django import DjangoObjectType

from estaciones.Tipos_Estacion.models import Tipo_Estacion

class Tipo_EstacionType(DjangoObjectType):
    class Meta:
        model = Tipo_Estacion
