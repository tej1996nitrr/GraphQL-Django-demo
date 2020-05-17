import graphene
# from graphqlA import schema 
from ingredients import schema 
# class Mutation(schema.Mutation,graphene.ObjectType):
#     pass
class Query(schema.Query,graphene.ObjectType):
    pass    
class Mutation(ingredients.schema.Mutation, graphene.ObjectType):
    pass
schema = graphene.Schema(query=Query)
