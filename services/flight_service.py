import requests
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

class FlightService:
    @staticmethod
    def get_flight_info(flight_number):
        # Obtenir le temps actuel en Unix timestamp
        current_time = datetime.now(timezone.utc)
        begin_time = int((current_time - timedelta(hours=2)).timestamp())
        end_time = int((current_time + timedelta(hours=2)).timestamp())

        load_dotenv()
        api_key = os.environ.get('FLIGHTS_API_KEY')

        # Utiliser l'API OpenSky pour obtenir les informations de vol
        url = f"https://opensky-network.org/api/states/all"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # Chercher le vol correspondant
            for state in data['states']:
                if state[1] and state[1].strip() == flight_number:
                    print(state)
                    # Obtenir le temps d'arrivée estimé
                    # Par défaut, on ajoute 2 heures au temps actuel pour l'estimation
                    arrival_time = current_time + timedelta(hours=2)

                    # Calculer le temps restant en minutes
                    time_delta = arrival_time - current_time
                    remaining_duration = max(30, int(time_delta.total_seconds() / 60))

                    # Construire la réponse avec toutes les informations nécessaires
                    return {
                        'icao24': state[0],
                        'origin_country': state[2],
                        'callsign': state[1],
                        'latitude': state[6],
                        'longitude': state[5],
                        'altitude': state[7],
                        'velocity': state[9],
                        'heading': state[10],
                        'remaining_duration': remaining_duration,
                        'arrival_time': arrival_time.isoformat()
                    }

        return None