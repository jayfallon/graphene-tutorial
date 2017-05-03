import graphene
# import schema from countries
from countries.schema import CountryQuery
from countries.schema import ContinentQuery
from countries.schema import CountryMutation
from countries.schema import ContinentMutation

# define root schema
# define root query
class RootQuery(CountryQuery
        , ContinentQuery
        , graphene.ObjectType):
    pass

# define root mutation
class RootMutation(CountryMutation
        , ContinentMutation
        , graphene.ObjectType):
    pass    

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
