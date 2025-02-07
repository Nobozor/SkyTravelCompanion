import unittest
from unittest.mock import MagicMock

import sys
import os

# Ajouter le chemin vers le dossier 'services' à sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../services')))
from movie_service import MovieService

class TestMovieService(unittest.TestCase):
    def setUp(self):
        self.movie_service = MovieService()
        self.movie_service.tmdb_service.get_movies_by_duration = MagicMock()

    def test_get_recommendations_no_movies(self):
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = []
        recommendations = self.movie_service.get_recommendations(120, 'action')
        self.assertEqual(recommendations, [])

    def test_get_recommendations_with_movies(self):
        movies = [
            {'title': 'Movie 1', 'duration': 90},
            {'title': 'Movie 2', 'duration': 60},
            {'title': 'Movie 3', 'duration': 45}
        ]
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = movies
        recommendations = self.movie_service.get_recommendations(120, 'action')
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]['title'], 'Movie 1')

    def test_get_recommendations_exact_duration(self):
        movies = [
            {'title': 'Movie 1', 'duration': 60},
            {'title': 'Movie 2', 'duration': 60}
        ]
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = movies
        recommendations = self.movie_service.get_recommendations(120, 'action')
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]['title'], 'Movie 1')
        self.assertEqual(recommendations[1]['title'], 'Movie 2')

    def test_get_recommendations_exceeding_duration(self):
        movies = [
            {'title': 'Movie 1', 'duration': 100},
            {'title': 'Movie 2', 'duration': 30},
            {'title': 'Movie 3', 'duration': 20}
        ]
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = movies
        recommendations = self.movie_service.get_recommendations(120, 'action')
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]['title'], 'Movie 1')
        self.assertEqual(recommendations[1]['title'], 'Movie 3')
    
    def test_get_recommendations_no_movie_fits(self):
        movies = [
            {'title': 'Movie 1', 'duration': 100},
            {'title': 'Movie 2', 'duration': 75}
        ]
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = movies
        recommendations = self.movie_service.get_recommendations(60, 'action')
        self.assertEqual(recommendations, [])


if __name__ == '__main__':
    unittest.main()