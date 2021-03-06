# Generated by Django 3.2 on 2021-05-14 04:14

from django.db import migrations
from game.models import Card, Deck, DeckCard


def create_initial_cards(apps, schema_editor):
    """
    Create initial set of playing cards
    """
    card_instances = []

    for suit in Card.Suit.choices:
        for rank in Card.Rank.choices:
            card_instances.append(Card(suit=suit[0], rank=rank[0]))

    Card.objects.bulk_create(card_instances)


def create_standard_deck(apps, schema_editor):
    """
    Create a standard deck of playing cards
    """
    standard_deck, _ = Deck.objects.get_or_create(name="Standard")

    deck_card_instances = [DeckCard(deck=standard_deck, card=card) for card in Card.objects.all()]
    DeckCard.objects.bulk_create(deck_card_instances)


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_cards),
        migrations.RunPython(create_standard_deck),
    ]
