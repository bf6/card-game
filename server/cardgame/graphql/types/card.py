"""Card GraphQL types."""

from graphene_django import DjangoObjectType

from game.models import Card as CardModel


class Card(DjangoObjectType):
    """GraphQL type for the Card model."""

    class Meta:
        model = CardModel
        only_fields = ("suit", "rank")
