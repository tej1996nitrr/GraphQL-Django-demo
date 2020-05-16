import graphene
from graphqlA import schema 

class Mutation(schema.Mutation,graphene.ObjectType):
    pass
class Query(schema.Query,graphene.ObjectType):
    pass    
schema = graphene.Schema(query=Query,mutation=Mutation)
