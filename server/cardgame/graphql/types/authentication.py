"""Authentication mutations."""

import graphene
from django.contrib.auth import authenticate, login, logout


class LogoutUser(graphene.Mutation):
    """Authentication mutation, deletes the session."""

    success = graphene.Boolean()

    def mutate(self, info, **kwargs):
        """Log the user out from Django."""
        logout(info.context)
        return LogoutUser(success=True)


class LoginUser(graphene.Mutation):
    """
    Validates the credentials and creates the session
    """

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    success = graphene.Boolean()

    def mutate(self, info, username, password, **kwargs):
        """Log the user in"""
        user = authenticate(username=username, password=password)
        if user is not None:
            login(info.context, user)
            return LoginUser(success=True)
        else:
            return LoginUser(success=False)
