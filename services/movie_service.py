from typing import List, Dict
from services.tmdb_service import TMDBService
import random

class MovieService:
    def __init__(self):
        self.tmdb_service = TMDBService()

    def get_recommendations(self, flight_duration: int, category: str) -> List[Dict]:
        # Obtenir les films depuis TMDB
        movies = self.tmdb_service.get_movies_by_duration(flight_duration, category)

        if not movies:
            return []

        # Trier les films par durée (du plus long au plus court)
        #movies.sort(key=lambda x: x['duration'], reverse=True)
        random.shuffle(movies)

        # Sélectionner les films qui peuvent rentrer dans la durée du vol
        selected_movies = []
        remaining_duration = flight_duration
        for movie in movies:
            if movie['duration'] <= remaining_duration and not movie['duration'] == 0:
                # Calculer la durée cumulative
                if selected_movies:
                    cumulative_duration = selected_movies[-1]['cumulative_duration'] + movie['duration']
                else:
                    cumulative_duration = movie['duration']

                movie['cumulative_duration'] = cumulative_duration
                selected_movies.append(movie)
                remaining_duration -= movie['duration']

                # Si nous avons suffisamment de films pour couvrir au moins 90% du vol
                if remaining_duration <= 0.1 * flight_duration:
                    break

        return selected_movies