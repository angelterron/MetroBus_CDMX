import graphene

from graphene_django.filter import DjangoFilterConnectionField

from estaciones.Alcaldias.models import Alcaldia
from estaciones.Tipos_Estacion.models import Tipo_Estacion 
from estaciones.Estaciones.models import Estacion

from estaciones.Alcaldias.schema import AlcaldiaType
from estaciones.Tipos_Estacion.schema import Tipo_EstacionType
from estaciones.Estaciones.schema import EstacionType


class Query(graphene.ObjectType):
    alcaldias = graphene.List(AlcaldiaType)
    tipos_estacion = graphene.List(Tipo_EstacionType)        
    estaciones = graphene.List( 
        EstacionType, # Se define el tipo de dato que tendra el objeto
        alcaldiaId = graphene.Int(), # Se define un argumento de tipo entero para filtrar por alcaldia
        id = graphene.Int(), # Se define un argumento de tipo entero para filtrar por id
    )


    def resolve_alcaldias(self, info, **kwargs):
        """
        Función para definir que devolvera el objeto alcaldias
        """

        # Regresa todas las alcaldias
        return Alcaldia.objects.all()
    
    def resolve_tipos_estacion(self, info, **kwargs):
        """
        Función para definir que devolvera el objeto tipos_estacion
        """
        # Regresa todos los tipos de estación
        return Tipo_Estacion.objects.all()

    def resolve_estaciones(self, info, alcaldiaId = None, id = None , **kwargs):
        """
        Función para definir que devolvera el objeto estaciones
        """
        # Si el argumento alcaldiaId es enviado, se filtran las estaciones por id de alcaldia
        if alcaldiaId:
            return Estacion.objects.filter(alcaldia_id = alcaldiaId)
        
        # Si el argumento Id es enviado, se filtran las estaciones por id
        if id:
            return Estacion.objects.filter(id = id)
        
        # Si ningún argumento es enviado, se devuelven todas las estaciones
        return Estacion.objects.all()