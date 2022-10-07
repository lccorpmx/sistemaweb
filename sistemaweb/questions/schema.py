import graphene
from graphene_django import DjangoObjectType

from .models import Question


class LinkType(DjangoObjectType):
    class Meta:
        model = Question


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Question.objects.all()