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

class CreateMovie(graphene.Mutation):
    class Arguments:
        movie_name = MovieInput(required=True)
    ok = graphene.Boolean()
    movie  = graphene.Field(MovieType)

    @staticmethod
    def mutate(root,info,input=None):
        ok = True
        actors=[]
        for actor_input in input.actors:
            actor = Actor.objects.get(pk=actor_input.id)
            if actor is None:
                return CreateMovie(ok=False,movie=None)
            actors.append(actor)
        movie_instance = Movie(title=input.title,year=input.year)
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateMovie(ok=ok,movie=movie_instance)
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        movie_name = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)
        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
              actor = Actor.objects.get(pk=actor_input.id)
              if actor is None:
                return UpdateMovie(ok=False, movie=None)
              actors.append(actor)
            movie_instance.title=input.title
            movie_instance.year=input.yearce.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)
        return UpdateMovie(ok=ok, movie=None)
class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)