from app import app
from unittest import TestCase
from flask import session, request
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_show_board(self):
        with self.client as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 class="counter"></h3>', html)
            self.assertIn('game_board', session)
            self.assertIsNone(session.get('totalGamesPlayed'))
            self.assertIsNone(session.get('highScore'))
            

    def test_check_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['game_board'] = [
                    ['D', 'O', 'G', 'G', 'G'],
                    ['I', 'G', 'G', 'G', 'G'],
                    ['C', 'R', 'A', 'P', 'P'],
                    ['B', 'L', 'A', 'H', 'H'],
                    ['B', 'L', 'A', 'H', 'H']
                ]
        response = self.client.get('/check-word?word=crap')
        self.assertEqual(response.json['result'], 'ok')

        response_2 = self.client.get('/check-word?word=dog')
        self.assertEqual(response_2.json['result'], 'ok')

    def test_post_score(self):
        with self.client as client:
            res = client.get("/post-score")

        self.assertEqual(res.status_code, 405)



