import unittest
from unittest.mock import patch, MagicMock
import builtins
from PRY2AYED20.src.recommendation_system import RecommendationSystem
import PRY2AYED20.src.main as main_module
from PRY2AYED20.src.artist import Artist

class TestMainFunction(unittest.TestCase):

    @patch('PRY2AYED20.src.main.input', create=True)
    @patch('PRY2AYED20.src.main.RecommendationSystem')
    def test_main(self, mock_recommendation_system, mock_input):
        mock_input.side_effect = ["Artist A"]
        mock_recommendation_instance = mock_recommendation_system.return_value
        mock_recommendation_instance.get_similar_artists.return_value = [
            Artist("Artist B", "Happy", "Rock"),
            Artist("Artist C", "Happy", "Rock")
        ]

        with patch('builtins.print') as mock_print:
            main_module.main()
            mock_print.assert_any_call("Similar artist to Artist A: Artist B")
            mock_print.assert_any_call("Mood: Happy")
            mock_print.assert_any_call("Genre: Rock")

if __name__ == '__main__':
    unittest.main()
