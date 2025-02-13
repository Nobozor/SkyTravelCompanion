import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import random

class SpotifyService:
    def __init__(self):
        load_dotenv()
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        client_redirection="http://localhost:5000"

        if not client_id or not client_secret:
            raise ValueError("Les clés API Spotify ne sont pas définies dans les variables d'environnement.")

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=client_redirection))

    def get_playlists(self, genre: str, limit: int = 10) -> list:
        """
        Récupère des playlists Spotify d'un genre donné et calcule leur durée totale.

        :param genre: Le genre musical recherché (ex: "rock", "jazz").
        :param limit: Nombre de playlists à récupérer.
        :return: Une liste de dictionnaires avec le nom de la playlist et sa durée totale en minutes.
        """
        offset = random.randint(0,100)
        results = self.sp.search(q=f"genre:{genre}", type='playlist', limit=limit, offset=offset)
        playlists = results.get('playlists', {}).get('items', [])
        playlist_w_good_format = []

        for playlist in playlists:
            if not playlist:
                continue
            else:
                playlist_id = playlist['id']
                total_tracks = playlist['tracks']['total']
                tracks = []
                                # Récupérer toutes les pistes de la playlist
                for i in range(0, total_tracks, 100):
                    tracks.extend(self.sp.playlist_tracks(playlist_id, offset=i, limit=100).get('items', []))

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
        random.shuffle(playlist_w_good_format) # Mélanger les playlists
        return playlist_w_good_format

# Exemple d'utilisation
if __name__ == "__main__":
    spotify_service = SpotifyService()
    genre = "rock"
    playlists = spotify_service.get_playlists(genre)
    
    for p in playlists:
        print(json.dumps(p, indent=4))