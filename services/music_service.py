from services.spotify_service import SpotifyService
import json
import asyncio

class MusicService:
    def __init__(self):
        self.spotifyObj = SpotifyService()

    async def get_recommendation(self, flight_duration: int, genre: str):

        enough_playlists = False
        count = 0
        nbr_iterations = 3

        while not enough_playlists:
            selected_playlists = []
            remaining_duration = flight_duration
            print(f"Iteration {count}")
            playlists = await self.spotifyObj.get_playlists(genre, flight_duration)  # get all playlists dicts
            print("Playlists have been pooled correctly")

            if not playlists:
                return []

            
            for playlist in playlists:
                print(f"Processing playlist: {playlist['name']}")
                print(f"Playlist duration : {playlist['duration_min']}")
                if playlist['duration_min'] <= remaining_duration:
                    if selected_playlists:
                        cumulated_duration = selected_playlists[-1]['cumulated_duration'] + playlist['duration_min']
                    else:
                        cumulated_duration = playlist['duration_min']
                    print(f"added playlist {playlist['name']} to selected playlists")
                    playlist['cumulated_duration'] = round(cumulated_duration, 2)
                    selected_playlists.append(playlist)
                    remaining_duration -= playlist['duration_min']
                    print(f"Remaining duration: {remaining_duration}")

                if remaining_duration <= 0.3 * flight_duration:
                    enough_playlists = True
                    print('Enough playlists')
                    break

            if not enough_playlists and count < nbr_iterations:
                print("No solution found, retrying")
                count += 1
                continue
            elif not enough_playlists and count >= nbr_iterations:
                print("Too many iterations")
                return []
            else:
                return selected_playlists

if __name__ == "__main__":
    music_service = MusicService()
    genre = "metal"
    flight_duration = 120
    recommendations = asyncio.run(music_service.get_recommendation(flight_duration, genre))

    for p in recommendations:
        print(json.dumps(p, indent=4))