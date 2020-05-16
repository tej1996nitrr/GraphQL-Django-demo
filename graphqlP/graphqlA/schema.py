import graphene
from graphene_django.types import DjangoObjectType
from . import models

class MessageType(DjangoObjectType):
    class Meta:
        model=models.Message
         
class Query(graphene.AbstractType):
    all_messages = graphene.List(MessageType)
    def resolve_all_messages(self,args,context,info):
        return models.Message.objects.all()