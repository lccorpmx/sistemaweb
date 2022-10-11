from asyncio import queues
import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from graphql import GraphQLError
from questions.models import Question, Vote
from django.db.models import Q
from .models import Question

# ...code
# Add after the LinkType
class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class Query(graphene.ObjectType):
    questions = graphene.List(
        QuestionType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    
    votes = graphene.List(VoteType)

    def resolve_questions(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Question.objects.all()

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


    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

# ...code
#1
class CreateQuestion(graphene.Mutation):
    id = graphene.Int()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        description = graphene.String()

    #3
    def mutate(self, info, description):
        user = info.context.user or None

        question = Question(
            description=description,
            posted_by=user,
        )
        question.save()

        return CreateQuestion(
            id=question.id,
            description=question.description,
            posted_by=question.posted_by,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    question = graphene.Field(QuestionType)

    class Arguments:
        question_id = graphene.Int()

    def mutate(self, info, question_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            question=question,
        )

        return CreateVote(user=user, question=question)

#4
class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    create_vote = CreateVote.Field()