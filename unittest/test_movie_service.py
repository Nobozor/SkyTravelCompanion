import unittest
from unittest.mock import MagicMock
import random

import sys
import os

# Ajouter le chemin vers le dossier 'services' à sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from services.movie_service import MovieService

class TestMovieService(unittest.TestCase):
    def setUp(self):
        # Initialise le service de films et simule la méthode de récupération des films
        self.movie_service = MovieService()
        self.movie_service.tmdb_service.get_movies_by_duration = MagicMock()
        random.seed(42)  # Fixe le seed pour rendre l'aléatoire déterministe pendant les tests

    def test_get_recommendations_no_movies(self):
        # Simule le cas où aucune donnée n'est retournée
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = []
        recommendations = self.movie_service.get_recommendations(120, 'action')
        self.assertEqual(recommendations, [])

    def test_get_recommendations_with_movies(self):
        # Liste de films à tester
        movies = [
            {'title': 'Movie 1', 'duration': 90},
            {'title': 'Movie 2', 'duration': 60},
            {'title': 'Movie 3', 'duration': 45}
        ]
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = movies
        recommendations = self.movie_service.get_recommendations(120, 'action')
        
        # Test que la durée totale des films ne dépasse pas la durée du vol
        total_duration = sum(movie['duration'] for movie in recommendations)
        self.assertLessEqual(total_duration, 120)
        
        # Test que les films sont bien dans les résultats
        titles = [movie['title'] for movie in recommendations]
        self.assertIn('Movie 3', titles)
        self.assertIn('Movie 2', titles)

    def test_get_recommendations_exact_duration(self):
        movies = [
            {'title': 'Movie 1', 'duration': 60},
            {'title': 'Movie 2', 'duration': 60}
        ]
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = movies
        recommendations = self.movie_service.get_recommendations(120, 'action')

        # Vérifie que la durée totale est exactement 120
        total_duration = sum(movie['duration'] for movie in recommendations)
        self.assertEqual(total_duration, 120)

        # Vérifie que les films sont dans les résultats
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]['title'], 'Movie 2')
        self.assertEqual(recommendations[1]['title'], 'Movie 1')

    def test_get_recommendations_exceeding_duration(self):
        movies = [
            {'title': 'Movie 1', 'duration': 100},
            {'title': 'Movie 2', 'duration': 30},
            {'title': 'Movie 3', 'duration': 20}
        ]
        self.movie_service.tmdb_service.get_movies_by_duration.return_value = movies
        recommendations = self.movie_service.get_recommendations(120, 'action')
        
        # Vérifie que la durée totale des films sélectionnés ne dépasse pas la durée du vol
        total_duration = sum(movie['duration'] for movie in recommendations)
        self.assertLessEqual(total_duration, 120)

        # Vérifie que les films sont bien dans les résultats
        titles = [movie['title'] for movie in recommendations]
        self.assertIn('Movie 2', titles)
        self.assertIn('Movie 3', titles)

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
