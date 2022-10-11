from re import U
import graphene
import graphene
import graphql_jwt


import questions.schema
import users.schema
import answers.schema


class Query(users.schema.Query ,questions.schema.Query, answers.schema.Query ,graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation ,questions.schema.Mutation,  answers.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)