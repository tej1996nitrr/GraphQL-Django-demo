import graphene
from graphene_django.types import DjangoObjectType
from . import models
from graphene_django.filter.fields  import DjangoFilterConnectionField
import json
class MessageType(DjangoObjectType):
    class Meta:
        model=models.Message
        filter_fields = {'message':['icontains']}# icontains=> can search for substring
        interfaces = (graphene.Node,)
         
class Query(graphene.AbstractType):
    all_messages = DjangoFilterConnectionField(MessageType)
    def resolve_all_messages(self,context,**kwargs):
        return models.Message.objects.all()

class CreateMessage(graphene.Mutation):
    class Input:
        message = graphene.String()

    form_errors = graphene.String()
    message = graphene.Field(lambda:MessageType)
    
    @staticmethod
    def mutate(root, args, context, info):
        if not context.user.is_authenticated():
            return CreateMessage(form_errors=json.dumps('Please login!'))
        message = models.Message.objects.create(
            user=context.user, message=args.get('message'))
        return CreateMessage(message=message, form_errors=None)
class Mutation(graphene.AbstractType):
    create_message = CreateMessage.Field()