import unittest
from unittest.mock import patch, Mock
import sys
import os

# Ajouter le chemin vers le dossier 'services' à sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from services.tmdb_service import TMDBService

class TestTMDBService(unittest.TestCase):
    @patch('services.tmdb_service.requests.get')
    def test_get_movies_by_duration(self, mock_get):
        # Mock response for discover movie
        mock_movie_response = Mock()
        mock_movie_response.status_code = 200
        mock_movie_response.json.return_value = {
            'results': [
                {'id': 1, 'title': 'Movie 1', 'overview': 'Overview 1', 'poster_path': '/path1.jpg', 'category': 'action', 'vote_average': 7.5},
                {'id': 2, 'title': 'Movie 2', 'overview': 'Overview 2', 'poster_path': '/path2.jpg', 'category': 'action', 'vote_average': 6.5}
            ]
        }

        # Mock response for movie details (runtime)
        mock_details_response_1 = Mock()
        mock_details_response_1.status_code = 200
        mock_details_response_1.json.return_value = {'runtime': 90}  # Movie 1 duration 90 min

        mock_details_response_2 = Mock()
        mock_details_response_2.status_code = 200
        mock_details_response_2.json.return_value = {'runtime': 120}  # Movie 2 duration 120 min

        # Utilisation de `side_effect` pour simuler deux appels successifs
        mock_get.side_effect = [mock_movie_response, mock_details_response_1, mock_details_response_2]

        service = TMDBService()
        movies = service.get_movies_by_duration(max_duration=100, genre='action')

        # Le test vérifie si le nombre de films est correct et que la durée est bien respectée
        self.assertEqual(len(movies), 1)  # Un seul film devrait être retourné
        self.assertEqual(movies[0]['title'], 'Movie 1')  # Movie 1 devrait être dans la liste
        self.assertEqual(movies[0]['duration'], 90)  # Durée du film 1 est 90 min

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
