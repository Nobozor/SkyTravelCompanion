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
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Flight ${flightNumber}</h5>
                        <p>Altitude: ${Math.round(data.altitude)} m</p>
                        <p>Speed: ${Math.round(data.velocity)} m/s</p>
                        <p>Heading: ${Math.round(data.heading)}°</p>
                    </div>
                </div>
            `;
        })
        .catch(error => console.error('Error:', error));
}
