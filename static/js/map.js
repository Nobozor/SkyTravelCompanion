let map = null;
let marker = null;

function initMap() {
    map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

function updateFlightPosition(flightNumber) {
    fetch(`/api/flight/${flightNumber}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Flight not found');
                return;
            }

            const position = [data.latitude, data.longitude];
            
            if (!marker) {
                marker = L.marker(position).addTo(map);
            } else {
                marker.setLatLng(position);
            }
            
            map.setView(position, 8);
            
            document.getElementById('flight-info').innerHTML = `
            <div class="container mt-4">
    <div class="card shadow-lg border-0 rounded-4">
        <div class="card-body">
            <h4 class="card-title" style="color: #f1c40f;"> <!-- Bleu aviation -->
                <i class="fas fa-plane"></i> Flight <span class="fw-bold">${flightNumber}</span>
            </h4>

            <hr>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <i class="fa-solid fa-mountain text-success"></i> 
                    <strong>Altitude:</strong> ${Math.round(data.altitude)} m
                </li>
                <li class="list-group-item">
                    <i class="fas fa-tachometer-alt text-danger"></i> 
                    <strong>Speed:</strong> ${Math.round(data.velocity)} m/s
                </li>
                <li class="list-group-item">
                    <i class="fa-regular fa-compass text-warning"></i> 
                    <strong>Heading:</strong> ${Math.round(data.heading)}°
                </li>
                <li class="list-group-item">
                    <i class="fa-solid fa-location-crosshairs text-info"></i> 
                    <strong>Latitude:</strong> ${data.latitude}, <strong>Longitude:</strong> ${data.longitude}
                </li>
                <li class="list-group-item">
                    <i class="fa-solid fa-globe text-primary"></i> 
                    <strong>Origin aircraft country:</strong> ${data.origin_country}
                </li>
            </ul>
        </div>
    </div>
</div>
            `;
        })
        .catch(error => console.error('Error:', error));
}
