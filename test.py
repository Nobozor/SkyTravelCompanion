import os
import sys
import time
import requests


                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-plane"></i> Flight ${flightNumber}</h5>
                        <p><i class="fa-solid fa-mountain"></i> Altitude: ${Math.round(data.altitude)} m</p>
                        <p><i class="fas fa-tachometer-alt"></i> Speed: ${Math.round(data.velocity)} m/s</p>
                        <p><i class="fa-regular fa-compass"></i> Heading: ${Math.round(data.heading)}°</p>
                        <p><i class="fa-solid fa-location-crosshairs"></i> Latitude: ${data.latitude} Longitude: ${data.longitude}</p>
                        <p><i class="fa-solid fa-globe"></i> Origin aircraft country: ${data.origin_country}</p>
                    </div>
                </div>



<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Flight Movie Companion</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Recherche de Vol</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/movies">Films</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>





.map-container {
    height: 500px;
    margin-bottom: 20px;
}

#map {
    height: 100%;
    width: 100%;
    border-radius: 8px;
}

#flight-info {
    margin-top: 20px;
}

.movie-search {
    margin-bottom: 30px;
}

.movie-card {
    height: 100%;
}

.notification {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;
}

.custom-navbar {
    background: linear-gradient(135deg, #121212, #1e1e1e); /* Fond plus marqué */
    border-bottom: 3px solid #00d4ff; /* Bordure pour bien séparer */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); /* Ombre plus marquée */
    padding: 12px 0;
}

.navbar-brand {
    font-size: 1.4rem;
    color: #ffffff;
    transition: transform 0.2s ease-in-out;
}

.navbar-brand:hover {
    transform: scale(1.05);
    color: #00d4ff;
}

.navbar-nav .nav-link {
    font-size: 1.1rem;
    padding: 12px 18px;
    color: rgba(255, 255, 255, 0.8);
    transition: all 0.3s ease;
    border-radius: 6px;
}

.navbar-nav .nav-link:hover {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.2);
}

.navbar-toggler {
    border: none;
    outline: none;
}

.navbar-toggler:focus {
    box-shadow: none;
}




function searchMovies(customDuration = null, customCategory = null) {
    const duration = customDuration || document.getElementById('flight-duration').value;
    const category = customCategory || document.getElementById('movie-category').value;

    fetch(`/api/movies?duration=${duration}&category=${category}`)
        .then(response => response.json())
        .then(movies => {
            const moviesContainer = document.getElementById('movie-recommendations');
            moviesContainer.innerHTML = '';

            if (movies.length === 0) {
                moviesContainer.innerHTML = `
                    <div class="alert alert-info">
                        Aucun film trouvé pour ces critères. Essayez une autre catégorie ou une durée différente.
                    </div>
                `;
                return;
            }

            const totalDuration = movies[movies.length - 1].cumulative_duration;
            const flightDuration = parseInt(duration);

            // Ajouter une barre de progression pour montrer la couverture du vol
            moviesContainer.innerHTML = `
                <div class="mb-4">
                    <h4>Utilisation du temps de vol</h4>
                    <div class="progress">
                        <div class="progress-bar" role="progressbar" 
                             style="width: ${(totalDuration / flightDuration) * 100}%"
                             aria-valuenow="${totalDuration}"
                             aria-valuemin="0"
                             aria-valuemax="${flightDuration}">
                            ${Math.round((totalDuration / flightDuration) * 100)}%
                        </div>
                    </div>
                    <small class="text-muted">
                        ${totalDuration} minutes sur ${flightDuration} minutes
                    </small>
                </div>
                <div class="row" id="movies-list"></div>
            `;

            const moviesList = document.getElementById('movies-list');
            movies.forEach((movie, index) => {
                const posterUrl = movie.poster_path 
                    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
                    : 'https://via.placeholder.com/500x750.png?text=Pas+d%27affiche';

                const movieCard = `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <img src="${posterUrl}" class="card-img-top" alt="${movie.title}">
                            <div class="card-body">
                                <h5 class="card-title">${movie.title}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">Film ${index + 1}</h6>
                                <div class="mb-2">
                                    <span class="badge bg-primary">${movie.vote_average}/10</span>
                                </div>
                                <p class="card-text">
                                    <strong>Durée:</strong> ${movie.duration} minutes<br>
                                    <strong>Temps cumulé:</strong> ${movie.cumulative_duration} minutes<br>
                                    ${movie.description}
                                </p>
                            </div>
                            <div class="card-footer">
                                <small class="text-muted">
                                    Commencer à: ${index === 0 ? '0' : movies[index-1].cumulative_duration} minutes
                                </small>
                            </div>
                        </div>
                    </div>
                `;
                moviesList.innerHTML += movieCard;
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('movie-recommendations').innerHTML = `
                <div class="alert alert-danger">
                    Une erreur est survenue lors de la recherche des films.
                </div>
            `;
        });
}



        {% if remaining_duration %}
        <div class="card mt-4">
            <div class="card-body">
                <h5 class="card-title">Informations de vol</h5>
                <p>Temps de vol restant: {{ remaining_duration }} minutes</p>
                <p>Pays d'origine de l'avion: {{ aircraft_origin_country }}</p>
                <p>Heure d'arrivée estimée: {{ arrival_time }}</p>

                <div class="movie-search mt-3">
                    <h6>Rechercher des films pour votre vol</h6>
                    <div class="form-group">
                        <label for="movie-category">Catégorie</label>
                        <select class="form-control" id="movie-category">
                            <option value="action">Action</option>
                            <option value="comedy">Comédie</option>
                            <option value="drama">Drame</option>
                            <option value="scifi">Science-Fiction</option>
                        </select>
                    </div>
                    <button class="btn btn-primary mt-3" onclick="searchFlightMovies()">Rechercher des films</button>
                </div>
                <div id="movie-recommendations" class="mt-3"></div>
            </div>
        </div>
        {% endif %}



<div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <a href="${playlist.playlist_url}" target="_blank">
                                <img src="${posterUrl}" class="card-img-top" alt="${playlist.name}">
                            </a>
                            <div class="card-body">
                                <h5 class="card-title">${playlist.name}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">Playlist n° ${index + 1}</h6>
                                <a href="${playlist.owner_url}" target="_blank" class="btn btn-primary">
                                    <p class="card-subtitle mb-2 text-muted">Owner : ${playlist.owner} minutes</h8>
                                </a>
                                <div class="mb-2">
                                    <span class="badge bg-primary">Tracks : ${playlist.total_tracks}</span>
                                </div>
                                <p class="card-text">
                                    <strong>Durée:</strong> ${playlist.duration_min} minutes<br>
                                    <strong>Temps cumulé:</strong> ${playlist.cumulated_duration} minutes<br>
                                    ${playlist.playlist_description}
                                </p>
                            </div>
                        </div>
                    </div>

from services.spotify_service import SpotifyService

class MusicService():
    def __init__(self):
        self.spotifyObj = SpotifyService()

    def get_recommendation(self, flight_duration: int, genre: str):
        enough_playlists = False
        count = 0
        nbr_iterations = 10
        while not enough_playlists:
            playlists = self.spotifyObj.get_playlists(genre) # get all playlists dicts
            
            if not playlists:
                return []
            selected_playlists = []
            remaining_duration = flight_duration
            for playlist in playlists:
                if playlist['duration_min'] <= remaining_duration:
                    if selected_playlists:
                        cumulated_duration = selected_playlists[-1]['duration_min'] + playlist['duration_min']
                    else:
                        cumulated_duration = playlist['duration_min']
                    
                    playlist['cumulated_duration'] = round(cumulated_duration, 2)
                    selected_playlists.append(playlist)
                    print(playlist['duration_min'])
                    print(remaining_duration)
                    print(selected_playlists)
                    remaining_duration -= playlist['duration_min']
                if remaining_duration <= 0.25 * flight_duration:
                    enough_playlists = True
                    print('enough playlists')
                    break
            if not enough_playlists and count < nbr_iterations:
                count +=1
                continue
            elif not enough_playlists and count >= nbr_iterations:
                return selected_playlists
            else:
                return selected_playlists
                
if __name__ == "__main__":
    musicServiceObj = MusicService()
    print(musicServiceObj.get_recommendation(120, 'metal'))