import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, redirect, request, session
import time
from google.cloud import storage
import datetime
import json

CLIENT_ID = "{YOUR SPOTIFY CLIENT ID}"
CLIENT_SECRET = "{YOUR SPOTIFY CLIENT SECRET ID}"

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = "Get track form spotify"
app.secret_key = "t67tr67tu8nye3qu89xu0"

@app.route("/")
def login():

    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirect_page():

    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('get_track', external=True))

@app.route("/getTrack")
def get_track():

    try:

        token_info = get_token()

    except:

        print("user not logged in")
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    tracks = sp.current_user_recently_played(limit=50)

    # send into data stage
    gcs = storage.Client()
    staging_area = gcs.bucket("arkan-spotify-analytics-stage-area")
    exist_files = [data.name for data in staging_area.list_blobs()]

    for track in tracks['items']:

        filename = track['played_at'].replace('T', ' ').split('.')[0]
        is_today = filename.split(' ')[0] == datetime.datetime.now().strftime("%Y-%m-%d")

        if is_today : 
            if filename not in exist_files:
                staging_area.blob(filename).upload_from_string(json.dumps(track), 'application/json')
                print("data has uploaded into staging area!")

            else:
                print("data has already in staging area!")
        else :
            print("data is not played today!")

    return "Finished!"

def get_token():

    token_info = session.get('token_info', None)

    if not token_info:
        
        redirect(url_for('login', external=False))

    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60

    if (is_expired):

        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():

    return SpotifyOAuth(

        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope='user-read-recently-played',
        redirect_uri=url_for('redirect_page', _external=True)

    )

if __name__ == "__main__":

    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
