function searchMusic( customCategory, customDuration ) {
    const duration = customDuration || document.getElementById('flight-duration').value;
    const category = customCategory || document.getElementById('music-category').value;
    const musicContainer = document.getElementById('music-recommendations');
    const loadingSpinner = document.getElementById('loading-spinner'); // Définir la variable loadingSpinner

   // Affiche le spinner et vide les résultats précédents
    loadingSpinner.style.display = 'block';
    musicContainer.innerHTML = '';

    fetch(`/api/music?duration=${duration}&category=${category}`)
        .then(response => response.json())
        .then(music => {
            loadingSpinner.style.display = 'none'; // Cache le spinner
            musicContainer.innerHTML = ''; // Vide l'affichage précédent

            if (music.length === 0) {
                musicContainer.innerHTML = `
                    <div class="alert alert-info">
                        Aucunes playlists n'ont été trouvées pour ces critères. Essayez une autre catégorie ou une durée différente.
                    </div>
                `;
                return;
            }

            const totalDuration = music[music.length - 1].cumulated_duration;
            const flightDuration = parseInt(duration);

            musicContainer.innerHTML = `
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
                <div class="row" id="playlist-list"></div>
            `;

            const playlistList = document.getElementById('playlist-list');
            music.forEach((playlist, index) => {
                const posterUrl = playlist.playlist_image
                    ? playlist.playlist_image
                    : 'https://placehold.co/600x400/white/black?text=no+cover';

                const musicCard = `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <a href="${playlist.playlist_url}" target="_blank">
                                <img src="${posterUrl}" class="card-img-top" alt="${playlist.name}">
                            </a>
                            <div class="card-body">
                                <h5 class="card-title">${playlist.name}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">Playlist n° ${index + 1}</h6>
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
                `;
                playlistList.innerHTML += musicCard;
            });
        })
        .catch(error => {
            console.error('Error:', error);
            loadingSpinner.style.display = 'none'; // Cache le spinner en cas d'erreur
            musicContainer.innerHTML = `
                <div class="alert alert-danger">
                    Une erreur est survenue lors de la recherche des playlists.
                </div>
            `;
        });
}