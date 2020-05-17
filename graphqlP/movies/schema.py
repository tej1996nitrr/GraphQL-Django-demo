import graphene
from graphene_django.types import DjangoObjectType,ObjectType
from .models import Movie,Actor

class ActorType(DjangoObjectType):
    class Meta:
        model = Actor
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class Query(ObjectType):
    actor = graphene.Field(ActorType,id=graphene.Int())
    movie = graphene.Field(MovieType,id=graphene.Int())
    actors = graphene.Field(ActorType)
    movies = graphene.Field(MovieType)

    def resolve_actor(self,info,**kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Actor.objects.get(pk=id)
        return None

    def resolve_movie(self,info,**kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Movie.objects.get(pk=id)
        return None

    def resove_movies(self,info,**kwargs):
        return Movie.objects.all()
    
    
    

