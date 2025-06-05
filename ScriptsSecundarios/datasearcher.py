# Este fue el codigo para la prueba inicial que permitio obtener imagenes de los artistas,
# e informacion como canciones destacadas usando el API de Spotify.
# Ahora programaprincipal.py, que es más avanzado, usa este programa para importar los permisos. No modificar.


import os

import spotipy
from flask import Flask, request, jsonify
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth

from ScriptsSecundarios import config

app = Flask(__name__)
CORS(app)

# Credenciales para autenticar
os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = config.SPOTIPY_REDIRECT_URI
username = "username"

# Permisos para acceder a la información
scope = "user-read-currently-playing user-read-playback-state"


@app.route('/search', methods=['GET', 'POST'])
def search():
    auth_manager = SpotifyOAuth(scope=scope)
    spotify_object = spotipy.Spotify(auth_manager=auth_manager)

    data = request.get_json()
    artist_name = data.get('term')

    search_results = spotify_object.search(artist_name, 1, 0, "artist")

    if search_results['artists']['items']:
        artist = search_results['artists']['items'][0]
        top_tracks = spotify_object.artist_top_tracks(artist['id'])['tracks'][:2]
        top_tracks_names = [track['name'] for track in top_tracks]
        top_tracks_urls = [track['external_urls']['spotify'] for track in top_tracks]

        return jsonify({'term': artist_name, 'image_url': artist['images'][0]['url'], 'top_tracks': top_tracks_names,
                        'top_tracks_urls': top_tracks_urls,
                        'genre': artist['genres'][0] if artist['genres'] else None})
    else:
        return jsonify({'term': artist_name, 'image_url': None, 'message': "Artist not found"})


if __name__ == '__main__':
    app.run(port=5000)
