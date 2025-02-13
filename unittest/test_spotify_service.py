import pytest
import aiohttp
from unittest.mock import patch, MagicMock
import sys
import os

# Ajouter le chemin vers le dossier 'services' à sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.spotify_service import SpotifyService

@pytest.fixture
def spotify_service():
    with patch('services.spotify_service.load_dotenv'):
        service = SpotifyService()
        service.CLIENT_ID = 'test_client_id'
        service.CLIENT_SECRET = 'test_client_secret'
        service.TOKEN = 'test_token'
        return service

def test_get_access_token(spotify_service):
    with patch('services.spotify_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {'access_token': 'test_access_token'}
        mock_post.return_value = mock_response

        token = spotify_service.get_access_token()
        assert token == 'test_access_token'

def test_search_playlists_by_genre(spotify_service):
    with patch('services.spotify_service.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'playlists': {'items': []}}
        mock_get.return_value = mock_response

        result = spotify_service.search_playlists_by_genre('rock')
        assert result == {'playlists': {'items': []}}

@pytest.mark.asyncio
async def test_get_playlists(spotify_service):
    with patch.object(spotify_service, 'search_playlists_by_genre') as mock_search, \
         patch.object(spotify_service, 'fetch_playlist_tracks') as mock_fetch:
        mock_search.return_value = {
            'playlists': {
                'items': [
                    {
                        'id': 'test_playlist_id',
                        'name': 'Test Playlist',
                        'description': 'Test Description',
                        'external_urls': {'spotify': 'http://test_playlist_url'},
                        'images': [{'url': 'http://test_image_url'}],
                        'tracks': {'total': 10},
                        'owner': {'display_name': 'Test Owner', 'external_urls': {'spotify': 'http://test_owner_url'}}
                    }
                ]
            }
        }
        mock_fetch.return_value = [{'track': {'duration_ms': 180000}}] * 10

        result = await spotify_service.get_playlists('rock', 120)
        assert len(result) == 1
        assert result[0]['name'] == 'Test Playlist'
        assert result[0]['duration_min'] == 30.0
