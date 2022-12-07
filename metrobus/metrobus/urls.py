from django.urls import path

from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .views import index



urlpatterns = [
    path('', index),
    path('consultas/', GraphQLView.as_view(graphiql=True)),
]
