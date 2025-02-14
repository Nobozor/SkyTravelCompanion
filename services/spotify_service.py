import os
import json
from dotenv import load_dotenv
import random
import asyncio
import base64
import requests
import aiohttp

class SpotifyService:
    def __init__(self):
        load_dotenv()
        self.CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.AUTH_URL = 'https://accounts.spotify.com/api/token'
        self.TOKEN = self.get_access_token()
        self.SEARCH_API_URL = 'https://api.spotify.com/v1/search'
        self.PLAYLIST_API_URL = 'https://api.spotify.com/v1/playlists/'

        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            raise ValueError("Les clés API Spotify ne sont pas définies dans les variables d'environnement.")
        if not self.TOKEN:
            raise ValueError("Le jeton d'accès Spotify n'a pas pu être obtenu.")

    def get_access_token(self):
        auth_header = base64.b64encode(f'{self.CLIENT_ID}:{self.CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {auth_header}'}
        data = {'grant_type': 'client_credentials'}
        response = requests.post(self.AUTH_URL, headers=headers, data=data)
        response_data = response.json()
        if 'access_token' in response_data:
            return response_data['access_token']
        else:
            raise Exception('Failed to get access token')

    def search_playlists_by_genre(self, genre, limit=20, offset=0):
        headers = {'Authorization': f'Bearer {self.TOKEN}'}
        url = f'{self.SEARCH_API_URL}?q=genre:{genre}&type=playlist&limit={limit}&offset={offset}'
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to search playlists by genre\n Status code: {response.status_code}\nResponse: {response.text}")

        return response.json()

    async def get_playlists(self, genre: str, flight_duration: int, limit: int = 40) -> list:
        """
        Récupère des playlists Spotify d'un genre donné et calcule leur durée totale.

        :param genre: Le genre musical recherché (ex: "rock", "jazz").
        :param limit: Nombre de playlists à récupérer.
        :return: Une liste de dictionnaires avec le nom de la playlist et sa durée totale en minutes.
        """
        offset = random.randint(0, 100)

        #results = self.sp.search(q=f"genre:{genre}", type='playlist', limit=limit, offset=offset)
        results = self.search_playlists_by_genre(genre, limit=limit, offset=offset)
        playlists = results.get('playlists', {}).get('items', [])
        playlist_w_good_format = []

        async with aiohttp.ClientSession() as session:
            for playlist in playlists:
                if not playlist:
                    continue
                if playlist['tracks']['total'] >= flight_duration / 2 or playlist['tracks']['total'] >= 300:
                    print("Playlist got too many tracks")
                    continue
                print("Playlist ok to add")
                playlist_id = playlist['id']
                total_tracks = playlist['tracks']['total']
                tracks = await self.fetch_playlist_tracks(session, playlist_id, total_tracks)
                total_duration_ms = sum(track['track']['duration_ms'] for track in tracks if track.get('track'))
                total_duration_min = total_duration_ms / 60000  # Convertir en minutes
                playlist_w_good_format.append({
                    'name': playlist['name'],
                    'duration_min': round(total_duration_min, 2),
                    'playlist_description': playlist['description'],
                    'playlist_url': playlist['external_urls']['spotify'],
                    'playlist_image': playlist['images'][0]['url'] if playlist['images'] else None,
                    'total_tracks': playlist['tracks']['total'],
                    'owner': playlist['owner']['display_name'],
                    'owner_url': playlist['owner']['external_urls']['spotify']
                })
        random.shuffle(playlist_w_good_format)  # Mélanger les playlists
        return playlist_w_good_format

    async def fetch_playlist_tracks(self, session, playlist_id, total_tracks):
        tracks = []
        headers = {
            'Authorization': f'Bearer {self.TOKEN}'
        }
        offset = 0
        limit = 100
        while offset < total_tracks:
            async with session.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit={limit}", headers=headers) as response:
                print(f"Fetching tracks for playlist {playlist_id} from {offset} to {offset + limit}")
                if response.status != 200:
                    print(f"Error fetching tracks for playlist {playlist_id}: {response.status}")
                    break
                data = await response.json()
                tracks.extend(data.get('items', []))
                offset += limit
        return tracks

# Exemple d'utilisation
if __name__ == "__main__":
    spotify_service = SpotifyService()
    genre = "rock"
    playlists = asyncio.run(spotify_service.get_playlists(genre, 120))
    for p in playlists:
        print(json.dumps(p, indent=4))