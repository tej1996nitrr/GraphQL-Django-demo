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

#define what fields can be used to change data in the API.
class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()

class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()

class CreateActor(graphene.Mutation):
    class Arguments:
        input=ActorInput(required=True)
    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)
    @staticmethod
    def mutate(root,info,input=None):
        ok = True
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(ok=ok,actor=actor_instance)

class UpdateActor(graphene.Mutation):
    class Arguments: #correspond to the input arguments for the mutator
        id = graphene.Int(required=True)
        actor_name = ActorInput(required=True)
    #The ok and actor properties make up the ActorPayload
    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)
        return UpdateActor(ok=ok, actor=None)
