import graphene

from estaciones import schema


class Query(schema.Query, graphene.ObjectType):
    # Esta clase heredará de múltiples Queries a medida 
    # que se comiencen a agregar aplicaciones al proyecto
    pass


schema = graphene.Schema(query=Query)