"""Test Model Methods"""

from django.contrib.auth.models import User
from django.test import TestCase

from game.exceptions import NoCardsLeftError
from game.models import Deck, UserGame


class DeckTestCase(TestCase):
    """Environment test cases."""

    def test_can_draw_cards(self):
        """Test that we can draw from the deck"""
        standard_deck = Deck.objects.get(name="Standard")
        cards = standard_deck.draw(10)
        self.assertEqual(len(cards), 10)

    def test_can_only_draw_each_card_once(self):
        """Test that we can only draw unique cards from the deck"""
        standard_deck = Deck.objects.get(name="Standard")

        # Draw 50 cards
        cards = standard_deck.draw(50)
        self.assertEqual(len(cards), 50)

        # Try to draw 10 more...
        additional_cards = standard_deck.draw(10, cards)

        # But we should only get 2
        self.assertEqual(len(additional_cards), 2)

    def test_draw_with_id_and_card(self):
        """Test that we can draw using id or Card instance"""
        standard_deck = Deck.objects.get(name="Standard")

        # Draw half of the deck
        cards = standard_deck.draw(26)

        # Get just their IDs
        cards = [c.id for c in cards]

        # Draw the second half
        additional_cards = standard_deck.draw(26, cards)

        # Should be 52 in total
        self.assertEqual(len(cards + additional_cards), 52)

    def test_cannot_draw_duplicate_cards(self):
        """Test that we handle drawing with duplicate inputs"""
        standard_deck = Deck.objects.get(name="Standard")

        # Draw half the deck
        cards = standard_deck.draw(26)

        # Duplicate the cards list
        cards = cards + cards

        # Draw the rest of the cards, notice we asked for 52
        additional_cards = standard_deck.draw(52, cards)

        # Should only have returned 26
        self.assertEqual(len(additional_cards), 26)


class GameTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Goku", password="Vegeta")

    def test_default_in_progress_standard_deck(self):
        """Test the default values in a game"""
        game = UserGame.objects.create(user=self.user)
        self.assertEqual(game.status, UserGame.GameStatus.IN_PROGRESS)
        self.assertEqual(game.deck.id, Deck.objects.get(name="Standard").id)

    def test_max_cards_drawn_throws_exception(self):
        """Test we can't draw from an empty game deck"""
        game = UserGame.objects.create(user=self.user)
        for _ in range(11):
            game.deal()

        # Should have drawn 52 cards by now
        self.assertEqual(len(game.cards_drawn), 52)

        # Should throw an exception if we try to deal again
        self.assertRaises(NoCardsLeftError, game.deal)

    def test_last_hand_ace_win(self):
        """Test that drawing an ace in the last hand wins"""
        standard_deck = Deck.objects.get(name="Standard")

        # Set up a game with 50 cards already drawn, in order of rank and suit
        game = UserGame.objects.create(
            user=self.user,
            cards_drawn=[deck_card.card.id for deck_card in standard_deck.cards.all()[:50]],
        )

        # Last hand should contain an Ace
        game.deal()

        self.assertEqual(game.status, UserGame.GameStatus.WIN)

    def test_last_hand_no_ace_lose(self):
        """Test that not drawing an ace in the last hand loses"""
        standard_deck = Deck.objects.get(name="Standard")

        # Set up a game with 50 cards already drawn, in reverse order of rank and suit
        game = UserGame.objects.create(
            user=self.user,
            cards_drawn=[
                deck_card.card.id for deck_card in standard_deck.cards.order_by("-id")[:50]
            ],
        )

        # Last hand should NOT contain an Ace
        game.deal()
        self.assertEqual(game.status, UserGame.GameStatus.LOSS)

    def test_reset_game(self):
        """Test resetting a game will return its cards to the deck"""
        game = UserGame.objects.create(user=self.user)
        game.deal()
        self.assertEqual(len(game.cards_drawn), 5)
        game.reset()
        self.assertEqual(len(game.cards_drawn), 0)
