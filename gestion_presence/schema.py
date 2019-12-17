import graphene
import graphql_jwt

import presence.schema


class Query(presence.schema.Query, graphene.ObjectType):
    pass


class Mutation(presence.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
