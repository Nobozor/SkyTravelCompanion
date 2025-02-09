import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

class TMDBService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get('TMDB_API_KEY')
        self.base_url = 'https://api.themoviedb.org/3'
        
    def get_movies_by_duration(self, max_duration: int, genre: str = None) -> List[Dict]:
        # Mapping des catégories vers les IDs de genre TMDB
        genre_mapping = {
            'action': 28,
            'comedy': 35,
            'drama': 18,
            'horror': 27,
            'scifi': 878
        }
        
        genre_id = genre_mapping.get(genre.lower()) if genre else None
        
        # Paramètres de base pour la requête
        params = {
            'api_key': self.api_key,
            'language': 'fr-FR',
            'sort_by': 'popularity.desc',
            'include_adult': False,
            'page': 1
        }
        
        if genre_id:
            params['with_genres'] = genre_id
            
        # Faire la requête à l'API
        response = requests.get(f'{self.base_url}/discover/movie', params=params)
        
        if response.status_code != 200:
            return []
            
        movies_data = response.json()
        movies = []
        
        for movie in movies_data.get('results', []):
            # Obtenir les détails du film pour avoir la durée
            movie_details = self.get_movie_details(movie['id'])
            if movie_details and movie_details.get('runtime', 0) <= max_duration:
                movies.append({
                    'tmdb_id': movie['id'],
                    'title': movie['title'],
                    'duration': movie_details.get('runtime', 0),
                    'category': genre,
                    'description': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'vote_average': movie['vote_average']
                })

        return movies
        
    def get_movie_details(self, movie_id: int) -> Dict:
        response = requests.get(
            f'{self.base_url}/movie/{movie_id}',
            params={'api_key': self.api_key, 'language': 'fr-FR'}
        )
        
        if response.status_code == 200:
            return response.json()
        return None
