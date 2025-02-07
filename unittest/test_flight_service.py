import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import sys
import os

# Ajouter le chemin vers le dossier 'services' à sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../services')))

# Maintenant, tu peux importer le module normalement
from flight_service import FlightService

class TestFlightService(unittest.TestCase):
    @patch('flight_service.requests.get')
    def test_get_flight_info_success(self, mock_get):
        # Mock the response from the OpenSky API
        mock_response = {
            'states': [
                ['abc123', 'FL123', None, None, None, 10.0, 20.0, 30000, None, 500, 180, None, None, None, None, None, None]
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        flight_number = 'FL123'
        result = FlightService.get_flight_info(flight_number)

        self.assertIsNotNone(result)
        self.assertEqual(result['callsign'], flight_number)
        self.assertEqual(result['latitude'], 20.0)
        self.assertEqual(result['longitude'], 10.0)
        self.assertEqual(result['altitude'], 30000)
        self.assertEqual(result['velocity'], 500)
        self.assertEqual(result['heading'], 180)
        self.assertGreaterEqual(result['remaining_duration'], 30)

    
    @patch('flight_service.requests.get')
    def test_get_flight_info_no_flight_found(self, mock_get):
        # Mock the response from the OpenSky API with no matching flight
        mock_response = {
            'states': [
                ['abc123', 'FL999', None, None, None, 10.0, 20.0, 30000, None, 500, 180, None, None, None, None, None, None]
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        flight_number = 'FL123'
        result = FlightService.get_flight_info(flight_number)

        self.assertIsNone(result)

    @patch('flight_service.requests.get')
    def test_get_flight_info_api_failure(self, mock_get):
        # Mock the response from the OpenSky API with a failure status code
        mock_get.return_value.status_code = 500

        flight_number = 'FL123'
        result = FlightService.get_flight_info(flight_number)

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()