from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from services.flight_service import FlightService
from services.movie_service import MovieService
from services.music_service import MusicService

load_dotenv()

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "supersecretkey"

PORT_LISTEN = os.environ.get("PORT_LISTEN") or 5000
LISTEN_HOST = os.environ.get("LISTEN_HOST") or '0.0.0.0'    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flight/<flight_number>')
def flight_info(flight_number):
    flight_service = FlightService()
    flight_data = flight_service.get_flight_info(flight_number)

    if flight_data:
        return render_template('flight.html', 
                         flight_number=flight_number,
                         aircraft_origin_country=flight_data['origin_country'],
                         remaining_duration=flight_data['remaining_duration'],
                         arrival_time=flight_data['arrival_time'])
    else:
        return render_template('flight.html', 
                        flight_number=flight_number,
                        remaining_duration=None,
                        arrival_time=None)

@app.route('/api/flight/<flight_number>')
def get_flight_data(flight_number):
    flight_service = FlightService()
    flight_data = flight_service.get_flight_info(flight_number)

    if flight_data:
        return jsonify(flight_data)

    return jsonify({'error': 'Flight not found'}), 404

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/api/movies')
def get_movie_recommendations():
    flight_duration = int(request.args.get('duration', 120))
    category = request.args.get('category', 'action')

    movie_service = MovieService()
    recommendations = movie_service.get_recommendations(flight_duration, category)
    return jsonify(recommendations)

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/api/music')
async def get_music_recommendations():
    flight_duration = int(request.args.get('duration', 120))
    category = request.args.get('category', 'rock')

    music_service = MusicService()
    recommendations = await music_service.get_recommendation(flight_duration, category)
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT_LISTEN, debug=True)