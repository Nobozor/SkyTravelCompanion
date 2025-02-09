function searchMovies(customDuration = null, customCategory = null) {
    const duration = customDuration || document.getElementById('flight-duration').value;
    const category = customCategory || document.getElementById('movie-category').value;
    const moviesContainer = document.getElementById('movie-recommendations');
    const loadingSpinner = document.getElementById('loading-spinner');

    // Affiche le spinner et vide les résultats précédents
    loadingSpinner.style.display = 'block';
    moviesContainer.innerHTML = '';

    fetch(`/api/movies?duration=${duration}&category=${category}`)
        .then(response => response.json())
        .then(movies => {
            loadingSpinner.style.display = 'none'; // Cache le spinner
            moviesContainer.innerHTML = ''; // Vide l'affichage précédent

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
            loadingSpinner.style.display = 'none'; // Cache le spinner en cas d'erreur
            moviesContainer.innerHTML = `
                <div class="alert alert-danger">
                    Une erreur est survenue lors de la recherche des films.
                </div>
            `;
        });
}
