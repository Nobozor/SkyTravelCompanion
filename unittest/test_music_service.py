import pytest
from services.music_service import MusicService
import pytest_mock
import asyncio

@pytest.fixture
def mock_spotify_service(mocker: pytest_mock.MockerFixture):
    mock_spotify = mocker.patch('services.music_service.SpotifyService')
    return mock_spotify

@pytest.fixture
def music_service(mock_spotify_service):
    return MusicService()

@pytest.mark.asyncio
async def test_get_recommendation_no_playlists(music_service, mock_spotify_service):
    mock_spotify_service().get_playlists.return_value = asyncio.Future()
    mock_spotify_service().get_playlists.return_value.set_result([])
    result = await music_service.get_recommendation(120, 'metal')
    assert result == []

@pytest.mark.asyncio
async def test_get_recommendation_enough_playlists(music_service, mock_spotify_service):
    mock_spotify_service().get_playlists.return_value = asyncio.Future()
    mock_spotify_service().get_playlists.return_value.set_result([
        {'name': 'Playlist 1', 'duration_min': 30},
        {'name': 'Playlist 2', 'duration_min': 60},
        {'name': 'Playlist 3', 'duration_min': 30}
    ])
    result = await music_service.get_recommendation(120, 'metal')
    assert len(result) > 0
    assert result[-1]['cumulated_duration'] <= 120

@pytest.mark.asyncio
async def test_get_recommendation_not_enough_playlists(music_service, mock_spotify_service):
    mock_spotify_service().get_playlists.return_value = asyncio.Future()
    mock_spotify_service().get_playlists.return_value.set_result([
        {'name': 'Playlist 1', 'duration_min': 30},
        {'name': 'Playlist 2', 'duration_min': 30}
    ])
    result = await music_service.get_recommendation(120, 'metal')
    assert result == []