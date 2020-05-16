import graphene
from graphene_django.types import DjangoObjectType
from . import models
from graphene_django.filter.fields  import DjangoFilterConnectionField
class MessageType(DjangoObjectType):
    class Meta:
        model=models.Message
        filter_fields = {'message':['icontains']}# icontains=> can search for substring
        interfaces = (graphene.Node,)
         
class Query(graphene.AbstractType):
    all_messages = DjangoFilterConnectionField(MessageType)
    def resolve_all_messages(self,context,**kwargs):
        return models.Message.objects.all()