import unittest
from unittest.mock import patch, Mock
import sys
import os

# Ajouter le chemin vers le dossier 'services' à sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from services.tmdb_service import TMDBService

class TestTMDBService(unittest.TestCase):
    @patch('services.tmdb_service.requests.get')
    def test_get_movie_details(self, mock_get):
        # Mock response for movie details
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'runtime': 90,
            'title': 'Movie 1',
            'overview': 'Overview 1',
            'poster_path': '/path1.jpg',
            'vote_average': 7.5
        }
        mock_get.return_value = mock_response

        service = TMDBService()
        movie_details = service.get_movie_details(1)

        self.assertIsNotNone(movie_details)
        self.assertEqual(movie_details['runtime'], 90)
        self.assertEqual(movie_details['title'], 'Movie 1')

    @patch('services.tmdb_service.requests.get')
    def test_get_movies_by_duration_no_results(self, mock_get):
        # Mock response for discover movie with no results
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response

        service = TMDBService()
        movies = service.get_movies_by_duration(max_duration=100, genre='action')

        self.assertEqual(len(movies), 0)

    @patch('services.tmdb_service.requests.get')
    def test_get_movies_by_duration_api_failure(self, mock_get):
        # Mock response for discover movie with API failure
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        service = TMDBService()
        movies = service.get_movies_by_duration(max_duration=100, genre='action')

        self.assertEqual(len(movies), 0)

if __name__ == '__main__':
    unittest.main()
