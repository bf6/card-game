"""Test API"""
import json

from django.contrib.auth.models import User

from graphene_django.utils.testing import GraphQLTestCase

from cardgame.schema import schema


class LoginAPITestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = User.objects.create_user(username="Peter", password="Parker1!")

    def test_login(self):
        """Test successful login"""
        response = self.query(
            """mutation {
                loginUser(username:"Peter", password:"Parker1!") {
                    success
                }
            }
        """,
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content["data"]["loginUser"]["success"], True)

    def test_bad_login(self):
        """Test unsuccessful login"""
        response = self.query(
            """mutation {
                loginUser(username:"Pedro", password:"Parquero2?") {
                    success
                }
            }""",
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content["data"]["loginUser"]["success"], False)


class GameAPITestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = User.objects.create_user(username="Peter", password="Parker1!")
        self.playGameQuery = """mutation {
                                playGame {
                                    gameId
                                    gameStatus
                                    createdAt
                                    updatedAt
                                    message
                                    cardsDealt
                                    cardsLeft
                                    cards {
                                    suit
                                    rank
                                    }
                                }
                            }"""
        self.loginQuery = """mutation {
                                loginUser(username:"Peter", password:"Parker1!") {
                                    success
                                }
                            }"""
        self.resetQuery = """mutation {
                                resetGame {
                                    success
                                }
                            }"""

    def test_play_game(self):
        """Basic test for playing a new game"""

        # Log in
        response = self.query(self.loginQuery)
        content = json.loads(response.content)
        self.assertEqual(content["data"]["loginUser"]["success"], True)

        # Start playing
        response = self.query(self.playGameQuery)
        content = json.loads(response.content)

        # Should have an in progress game with 5 cards dealt
        self.assertEqual(content["data"]["playGame"]["cardsDealt"], 5)
        self.assertEqual(content["data"]["playGame"]["gameStatus"], "IN_PROGRESS")

    def test_game_continuity(self):
        """Test that game state is persisted across requests"""
        self.query(self.loginQuery)

        response = self.query(self.playGameQuery)
        content = json.loads(response.content)["data"]["playGame"]

        # Draw once
        game_id = content["gameId"]
        self.assertEqual(content["cardsDealt"], 5)

        # Draw 3 more times
        self.query(self.playGameQuery)
        self.query(self.playGameQuery)
        response = self.query(self.playGameQuery)

        # Should be the same game, with 20 cards dealt
        content = json.loads(response.content)["data"]["playGame"]
        self.assertEqual(content["gameId"], game_id)
        self.assertEqual(content["cardsDealt"], 20)

    def test_new_game(self):
        """Tests that a new game begins when a game finishes"""
        self.query(self.loginQuery)

        # Draw all 52 cards
        for _ in range(11):
            response = self.query(self.playGameQuery)

        # Game should be over now
        content = json.loads(response.content)["data"]["playGame"]
        game_id = content["gameId"]
        self.assertNotEqual(content["gameStatus"], "IN_PROGRESS")
        self.assertEqual(content["cardsLeft"], 0)

        # Draw again
        response = self.query(self.playGameQuery)

        # Game should be different
        content = json.loads(response.content)["data"]["playGame"]
        self.assertNotEqual(content["gameId"], game_id)
        self.assertEqual(content["cardsDealt"], 5)

    def test_reset_game(self):
        """Test that we can reset an in-progress game"""
        self.query(self.loginQuery)

        # Draw 10 cards
        for _ in range(2):
            response = self.query(self.playGameQuery)

        content = json.loads(response.content)["data"]["playGame"]
        game_id = content["gameId"]
        self.assertEqual(content["cardsLeft"], 42)

        # Reset the game
        response = self.query(self.resetQuery)

        # Deal again
        response = self.query(self.playGameQuery)

        # Game should be same, but dealt cards restarted
        content = json.loads(response.content)["data"]["playGame"]
        self.assertEqual(content["gameId"], game_id)
        self.assertEqual(content["cardsDealt"], 5)
