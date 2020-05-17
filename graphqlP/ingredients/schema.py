import graphene
from graphene_django.types import DjangoObjectType
from .models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class Query(object):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)


    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()
    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

class AddCategory(graphene.Mutation):
    class Arguments:
        categoryName = graphene.String(required=True)
    category = graphene.Field(CategoryType)
    def mutate(self,info,categoryName):
        _category = Category.objects.create(name=categoryName)
        return AddCategory(category=_category)
        
class Mutation(object):
    add_category = AddCategory.Field()