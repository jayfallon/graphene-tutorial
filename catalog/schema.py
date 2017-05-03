import graphene
from countries.schema import CountryQuery
from countries.schema import ContinentQuery
from countries.schema import CountryMutation
from countries.schema import ContinentMutation

class RootQuery(CountryQuery
        , ContinentQuery
        , graphene.ObjectType):
    pass

class RootMutation(CountryMutation
        , ContinentMutation
        , graphene.ObjectType):
    pass    

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
