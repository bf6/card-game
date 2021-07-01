"""GraphQL schema specific to this app."""

import graphene

from .types.authentication import LoginUser, LogoutUser
from .types.game import PlayGame, ResetGame
from .types.user import User as UserNode


class Query(graphene.ObjectType):
    """Queries specific to cardgame app."""

    class Meta:
        abstract = True

    me = graphene.Field(UserNode)

    def resolve_me(self, info, **kwargs):
        """Return the current logged in user."""
        return info.context.user


class Mutation(graphene.ObjectType):
    """Mutations specific to cardgame app."""

    class Meta:
        abstract = True

    login_user = LoginUser.Field(description="Log the user in.")
    logout_user = LogoutUser.Field(description="Log the user out.")
    play_game = PlayGame.Field(description="Start a new game or continue playing the current one.")
    reset_game = ResetGame.Field(description="Reset the current game.")
