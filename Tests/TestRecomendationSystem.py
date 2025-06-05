import unittest
from unittest.mock import patch, MagicMock
from PRY2AYED20.src.recommendation_system import RecommendationSystem
from PRY2AYED20.src.artist import Artist

class TestRecommendationSystem(unittest.TestCase):

    @patch('PRY2AYED20.src.recommendation_system.GraphDatabase.driver')
    def test_get_similar_artists(self, mock_driver):
        mock_session = MagicMock()
        mock_run = mock_session.run
        mock_driver.return_value.session.return_value.__enter__.return_value = mock_session

        mock_run.return_value = [
            {"name": "Artist B", "mood": "Happy", "genre": "Rock"},
            {"name": "Artist C", "mood": "Happy", "genre": "Rock"}
        ]

        recommendation_system = RecommendationSystem()
        similar_artists = recommendation_system.get_similar_artists("Artist A")

        self.assertEqual(len(similar_artists), 2)
        self.assertEqual(similar_artists[0].name, "Artist B")
        self.assertEqual(similar_artists[0].mood, "Happy")
        self.assertEqual(similar_artists[0].genre, "Rock")

if __name__ == '__main__':
    unittest.main()
