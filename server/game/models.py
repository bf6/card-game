from collections import Counter
import random

from django.contrib.auth.models import User as UserModel
from django.contrib.postgres.fields import ArrayField
from django.db import models

from .exceptions import NoCardsLeftError


class Card(models.Model):
    """Card Model"""

    class Suit(models.TextChoices):
        CLUB = "CLUB"
        DIAMOND = "DIAMOND"
        HEART = "HEART"
        SPADE = "SPADE"

    class Rank(models.TextChoices):
        TWO = "TWO"
        THREE = "THREE"
        FOUR = "FOUR"
        FIVE = "FIVE"
        SIX = "SIX"
        SEVEN = "SEVEN"
        EIGHT = "EIGHT"
        NINE = "NINE"
        TEN = "TEN"
        JACK = "JACK"
        QUEEN = "QUEEN"
        KING = "KING"
        ACE = "ACE"

    rank = models.CharField(max_length=16, choices=Rank.choices)
    suit = models.CharField(max_length=16, choices=Suit.choices)

    def __str__(self):
        """e.g. Ace of Spades"""
        return f"{self.rank.title()} of {self.suit.title()}s"


class DeckCard(models.Model):
    """The relationship between an abstract Card and a Deck"""

    card = models.ForeignKey("game.Card", on_delete=models.CASCADE)
    deck = models.ForeignKey("game.Deck", on_delete=models.CASCADE, related_name="cards")
    quantity = models.IntegerField(default=1)


class Deck(models.Model):
    """
    A Deck is a collection of Cards each having a quantity

    This model mainly provides a stateless method for drawing cards
    given an optional list of cards that have already been dealt.
    """

    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} Deck"

    def _get_card_counter(self):
        """
        Returns a Counter with quantities of each card in the deck
        """
        return Counter({deck_card.card.id: deck_card.quantity for deck_card in self.cards.all()})

    def draw(self, count: int, drawn: list = None):
        """
        Method that returns up to `count` Card objects from this Deck

        Optional argument `drawn` is a list of
        `Card` objects or ids of cards that have already been
        drawn from this deck.
        """
        card_counter = self._get_card_counter()

        if drawn:
            for card in drawn:
                if isinstance(card, Card):
                    card_counter[card.id] -= 1
                else:
                    card_counter[card] -= 1

        choices = []
        for _ in range(count):
            # Counter.elements() handily ignores elements with values less than 1
            try:
                card = random.choice(list(card_counter.elements()))
                card_counter[card] -= 1
                choices.append(card)
            except IndexError:
                break

        return list(Card.objects.filter(id__in=choices))


def get_default_deck():
    """Returns the standard 52-card Deck instance"""
    return Deck.objects.get(name="Standard").id


class UserGame(models.Model):
    """
    User Game Model

    Essentially a state machine that keeps a list of card ids
    drawn so far.
    """

    class GameStatus(models.TextChoices):
        WIN = "WIN"
        LOSS = "LOSS"
        IN_PROGRESS = "IN_PROGRESS"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="games")
    cards_drawn = ArrayField(models.IntegerField(), default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deck = models.ForeignKey(
        "game.Deck", on_delete=models.SET_NULL, null=True, default=get_default_deck
    )
    status = models.CharField(
        max_length=16, choices=GameStatus.choices, default=GameStatus.IN_PROGRESS
    )

    def deal(self):
        """
        Method to deal a hand for the current game.

        Raises an exception if there are no cards left to deal.

        If it's the final hand, updates status to "WIN" or "LOSS"
        if there is an Ace present.

        Returns a list of dealt `Card` objects.
        """
        deck_card_count = self.deck.cards.count()
        if len(self.cards_drawn) == deck_card_count:
            raise NoCardsLeftError("There are no cards left in the deck for this game.")

        cards = self.deck.draw(5, self.cards_drawn)
        self.cards_drawn += [c.id for c in cards]

        if len(self.cards_drawn) == deck_card_count:
            if any(filter(lambda card: card.rank == Card.Rank.ACE, cards)):
                self.status = self.GameStatus.WIN
            else:
                self.status = self.GameStatus.LOSS

        self.save()
        return cards

    def reset(self):
        """Reset this game by returning the cards to the deck"""
        self.cards_drawn = []
        self.save()

    @property
    def cards_left(self):
        """Number of cards left in the deck"""
        return self.deck.cards.count() - self.cards_dealt

    @property
    def cards_dealt(self):
        """Number of cards drawn from deck so far"""
        return len(self.cards_drawn)
