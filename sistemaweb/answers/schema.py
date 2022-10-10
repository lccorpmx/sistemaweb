from asyncio import queues
from re import A
from zipapp import create_archive
import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from graphql import GraphQLError
from answers.models import Answer
from django.db.models import Q
from .models import Answer

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer


class Query(graphene.ObjectType):
    answers = graphene.List(
        AnswerType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    

    def resolve_answers(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Answer.objects.all()

        if search:
            filter = (
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

# ...code
#1
class CreateAnswer(graphene.Mutation):
    id = graphene.Int()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        description = graphene.String()

    #3
    def mutate(self, info, description):
        user = info.context.user or None

        answer = Answer(
            description=description,
            posted_by=user,
        )
        answer.save()

        return CreateAnswer(
            id=answer.id,
            description=answer.description,
            posted_by=answer.posted_by,
        )


#4
class Mutation(graphene.ObjectType):
    create_answer = CreateAnswer.Field()