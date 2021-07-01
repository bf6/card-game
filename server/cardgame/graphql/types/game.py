"""Game mutations"""

import graphene

from game.models import UserGame

from .card import Card as CardNode


class PlayGame(graphene.Mutation):
    """
    Mutation for Dealing Cards.
    """

    cards = graphene.List(CardNode)
    game_status = graphene.String()
    game_id = graphene.ID()
    cards_dealt = graphene.Int()
    cards_left = graphene.Int()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    in_progress = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, **kwargs):
        """
        Deal cards for the current game.
        If there is an in progress game for the authenticated user, continue playing.
        Otherwise, creates a new game.
        """
        game, _ = UserGame.objects.get_or_create(
            user=info.context.user, status=UserGame.GameStatus.IN_PROGRESS
        )
        cards = game.deal()

        message = None
        if game.status == UserGame.GameStatus.WIN:
            message = "You Win"
        elif game.status == UserGame.GameStatus.LOSS:
            message = "You Lose, Sucker"

        return PlayGame(
            cards=cards,
            game_status=game.status,
            game_id=game.id,
            created_at=game.created_at,
            updated_at=game.updated_at,
            cards_dealt=game.cards_dealt,
            cards_left=game.cards_left,
            message=message,
        )


class ResetGame(graphene.Mutation):
    """
    Mutation for resetting the in progress game
    """

    success = graphene.Boolean()

    def mutate(self, info, **kwargs):
        """
        Reset the current game (or starts a new one if there is no game in progress)
        """
        game, created = UserGame.objects.get_or_create(
            user=info.context.user, status=UserGame.GameStatus.IN_PROGRESS
        )
        if not created:
            game.reset()

        return ResetGame(success=True)
