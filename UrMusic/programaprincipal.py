# Esta es una aplicacion usando Flask
# que permite buscar artistas en Spotify y obtener información sobre ellos.
import os
import sys

import spotipy
from flask import Flask, url_for
from flask import request, render_template, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from spotipy import SpotifyOAuth

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from PRY2AYED20.src.recommendation_system import RecommendationSystem
from ScriptsSecundarios.datasearcher import scope
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

recommendation_system = RecommendationSystem()

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'databases/satisfactionDatabase.db')

os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)


with app.app_context():
    db.create_all()

with app.app_context():
    db.create_all()
    if not Counter.query.first():
        db.session.add(Counter())
        db.session.commit()


@app.route('/api/counter', methods=['GET', 'POST'])
def counter():
    counter = Counter.query.first()
    if request.method == 'POST':
        if request.json.get('like') is not None:
            if request.json.get('like'):
                counter.likes += 1
            else:
                counter.likes -= 1
        elif request.json.get('dislike') is not None:
            if request.json.get('dislike'):
                counter.dislikes += 1
            else:
                counter.dislikes -= 1
        db.session.commit()

    total_votes = counter.likes + counter.dislikes
    satisfaction_percentage = (counter.likes / total_votes) * 100 if total_votes > 0 else 0

    return jsonify({'likeCounter': counter.likes, 'dislikeCounter': counter.dislikes,
                    'satisfactionPercentage': satisfaction_percentage})


@app.route('/')
def index():
    css_url = url_for('static', filename='style.css')
    favicon_url = url_for('static', filename='static/favicon/apple-touch-icon.png')
    return render_template('index.html', css_url=css_url, favicon_url=favicon_url)


@app.route('/resultados')
def resultados():
    artist_name = request.args.get('artist')

    # Verificar que el artista existe en nuestra base de datos.
    artist_exists = recommendation_system.artist_exists_in_database(artist_name)

    if artist_exists:
        # Si el artista existe, obtener la data del API de Spotify
        auth_manager = SpotifyOAuth(scope=scope)
        spotify_object = spotipy.Spotify(auth_manager=auth_manager)

        search_results = spotify_object.search(artist_name, 1, 0, "artist")
        artist = search_results['artists']['items'][0]
        top_tracks = spotify_object.artist_top_tracks(artist['id'])['tracks'][:2]
        top_tracks_names = [track['name'] for track in top_tracks]
        top_tracks_urls = [track['external_urls']['spotify'] for track in top_tracks]

        artist_data = {'name': artist_name, 'image_url': artist['images'][0]['url'], 'top_tracks': top_tracks_names,
                       'top_tracks_urls': top_tracks_urls, 'genre': artist['genres'][0] if artist['genres'] else None, 'found': True}
    else:
        # If the artist doesn't exist, set the 'found' key to False.
        artist_data = {'name': artist_name, 'image_url': None, 'message': "Artist not found", 'found': False}

    print(artist_data)  # Add this line
    css_url = url_for('static', filename='style.css')
    favicon_url = url_for('static', filename='favicon/apple-touch-icon.png')
    favicon_32_url = url_for('static', filename='favicon/favicon-32x32.png')
    favicon_16_url = url_for('static', filename='favicon/favicon-16x16.png')
    js_url = url_for('static', filename='main2.js')
    return render_template('resultados.html', artist=artist_data, css_url=css_url, favicon_url=favicon_url,
                           favicon_32_url=favicon_32_url, favicon_16_url=favicon_16_url, js_url=js_url)


@app.route('/api/recommend', methods=['POST', 'OPTIONS'])
def recommend():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = resp.headers
        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Headers'] = '*'
        headers['Access-Control-Allow-Methods'] = '*'
        return resp

    # Obtener recomendaciones de artistas similares.
    artist_name = request.json['artist']
    similar_artists = recommendation_system.get_similar_artists(artist_name)
    similar_artist_names = [artist for artist in similar_artists]
    return jsonify(similar_artist_names)


@app.route('/search', methods=['POST', 'OPTIONS'])
@cross_origin()
def search():
    artist_name = request.json.get('term')
    if not artist_name:
        return jsonify({'error': 'Artist name is required'}), 400

    auth_manager = SpotifyOAuth(scope=scope)
    spotify_object = spotipy.Spotify(auth_manager=auth_manager)

    # Remover espacio en el nombre del artista para hacer la búsqueda.
    artist_name_no_spaces = artist_name.replace(" ", "")
    search_results = spotify_object.search(artist_name_no_spaces, 1, 0, "artist")

    if search_results['artists']['items']:
        artist = search_results['artists']['items'][0]
        top_tracks = spotify_object.artist_top_tracks(artist['id'])['tracks'][:2]
        top_tracks_names = [track['name'] for track in top_tracks]
        top_tracks_urls = [track['external_urls']['spotify'] for track in top_tracks]

        return jsonify({'term': artist_name, 'image_url': artist['images'][0]['url'], 'top_tracks': top_tracks_names,
                        'top_tracks_urls': top_tracks_urls, 'genre': artist['genres'][0] if artist['genres'] else None})
    else:
        return jsonify({'term': artist_name, 'image_url': None, 'message': "Artist not found"})


if __name__ == '__main__':
    app.run(host='localhost', port=5000)