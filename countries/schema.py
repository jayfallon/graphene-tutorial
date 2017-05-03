# import graphene
from graphene import AbstractType
from graphene import Field
from graphene import Node
from graphene import ClientIDMutation
from graphene import String
from graphene import Float

# import graphene_django
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

# import models
from .models import Continent
from .models import Country

# import relay module
from graphql_relay.node.node import from_global_id

# define node classes
class ContinentNode(DjangoObjectType):
    class Meta:
        model = Continent
        interfaces = (Node, )
        filter_fields = ['name', 'countries']

class CountryNode(DjangoObjectType):
    class Meta:
        model = Country
        interfaces = (Node, )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'capital': ['exact', 'icontains'],
            'continent': ['exact'],
        }

# define mutation, update and delete classes

# creates new continent
class NewContinent(ClientIDMutation):
    continent = Field(ContinentNode)
    class Input:
        name = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Continent(
             name = input.get('name') ,
        )
        temp.save()
        return NewContinent(continent=temp)

# creates new country
class NewCountry(ClientIDMutation):
    country = Field(CountryNode)
    class Input:
        name = String()
        capital = String()
        continent = String()
    
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        country = Country(
            name = input.get('name'),
            capital = input.get('capital'),
            continent = Continent.objects.get(name=input.get('continent'))            
        )
        country.save()
        return NewCountry(country=country)

# updates country
class UpdateCountry(ClientIDMutation):
    country = Field(CountryNode)
    class Input:
        id = String()
        name = String()
        capital = String()
    
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        country = Country.objects.get(pk=from_global_id(input.get('id'))[1])
        country.name=input.get('name')
        country.capital=input.get('capital')
        country.save()
        return UpdateCountry(country=country)

# deletes country
class RemoveCountry(ClientIDMutation):
    country = Field(CountryNode)
    class Input:
        id = String()
        name = String()
        author = String()
    
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        country = Country.objects.get(pk=from_global_id(input.get('id'))[1])
        country.name=input.get('name')
        country.author=input.get('author')
        country.delete()
        return RemoveCountry(country=country)        

# define query classes
class ContinentQuery(AbstractType):
     continent = DjangoFilterConnectionField(ContinentNode)
 
class CountryQuery(AbstractType):
     country = Node.Field(CountryNode)
     all_countries = DjangoFilterConnectionField(CountryNode)

class ContinentMutation(AbstractType):
	new_continent = NewContinent.Field()

class CountryMutation(AbstractType):
	new_Country = NewCountry.Field()
	update_country = UpdateCountry.Field()
	remove_country = RemoveCountry.Field()
