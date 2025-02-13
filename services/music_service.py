from services.spotify_service import SpotifyService
import json

class MusicService:
    def __init__(self):
        self.spotifyObj = SpotifyService()

    def get_recommendation(self, flight_duration: int, genre: str):
        enough_playlists = False
        count = 0
        nbr_iterations = 10
        selected_playlists = []

        while not enough_playlists:
            playlists = self.spotifyObj.get_playlists(genre)  # get all playlists dicts

            if not playlists:
                return []

            remaining_duration = flight_duration
            for playlist in playlists:
                if playlist['duration_min'] <= remaining_duration:
                    if selected_playlists:
                        cumulated_duration = selected_playlists[-1]['cumulated_duration'] + playlist['duration_min']
                    else:
                        cumulated_duration = playlist['duration_min']

                    playlist['cumulated_duration'] = round(cumulated_duration, 2)
                    selected_playlists.append(playlist)
                    remaining_duration -= playlist['duration_min']

                    # Debug prints
                    print(f"Playlist duration: {playlist['duration_min']}")
                    print(f"Remaining duration: {remaining_duration}")
                    print(f"Selected playlists: {selected_playlists}")

                    if remaining_duration <= 0.25 * flight_duration:
                        enough_playlists = True
                        print('Enough playlists')
                        break

            if enough_playlists:
                return selected_playlists
            elif not enough_playlists and count < nbr_iterations:
                count += 1
                continue
            elif not enough_playlists and count >= nbr_iterations:
                return selected_playlists
            else:
                return selected_playlists

if __name__ == "__main__":
    music_service = MusicService()
    genre = "metal"
    flight_duration = 120
    recommendations = music_service.get_recommendation(flight_duration, genre)

    for p in recommendations:
        print(json.dumps(p, indent=4))