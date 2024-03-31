
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyPKCE
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import uuid  # Import the UUID module to generate unique IDs for each user


import streamlit as st
from datetime import datetime
import time


# Generate a unique identifier for the current user session
user_session_id = str(uuid.uuid4())

SPOTIPY_CLIENT_ID='23a9fab99eee4d3a81a64dcbbe35b546'
SPOTIPY_CLIENT_SECRET='b2eb7cde914b4aaaaec6f4b542378dfa'
SPOTIPY_REDIRECT_URI='http://localhost:3000'

scope = ["user-library-read", "user-modify-playback-state", 
         "user-top-read", "user-read-recently-played", "user-read-playback-state"]

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# cid = SPOTIPY_CLIENT_ID
# secret = SPOTIPY_CLIENT_SECRET
# scope = "playlist-modify-public"
# token = util.prompt_for_user_token('USERNAME_TO_AUTHORIZE',scope,client_id=cid,
#                                    client_secret=secret,redirect_uri='http://localhost:3000')
# sp = spotipy.Spotify(auth=token)

# # Create a Spotify client object with the SpotifyOAuth authentication manager
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
#                                                client_id=SPOTIPY_CLIENT_ID, 
#                                                client_secret=SPOTIPY_CLIENT_SECRET, 
#                                                redirect_uri=SPOTIPY_REDIRECT_URI,
#                                                cache_path=f'.spotifycache_{user_session_id}'))




#works to require login every time it is a new user
sp = spotipy.Spotify(auth_manager=SpotifyPKCE(scope=scope, 
                                               client_id=SPOTIPY_CLIENT_ID,  
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               cache_path=f'.spotifycache_{user_session_id}'))

#testing newmethod
        


# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, 
#                                                client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))





def get_recommendations(track_name):
    # Get track URI
    print("flag")
    results = sp.search(q=track_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']

    # Get recommended tracks
    num_recommendations = 5
    recommendations = sp.recommendations(seed_tracks=[track_uri], limit=num_recommendations)['tracks']
    return recommendations


#generate web app

    


st.title("Music Recommendation System")
track_name = st.text_input("Enter a song name:")


#if user inputs a track name display 5 recommendations based on that song and 
#play top recommendation on availble device
if track_name:
    recommendations = get_recommendations(track_name)
    st.write("Recommended songs:")
    for track in recommendations:
        st.header(track['name'])
        st.image(track['album']['images'][0]['url'])

    


    #begin playback of top song
    uri = recommendations[0]['uri']
    devices = sp.devices()
    #print available devices and their status
    print(f"\n\nnum devices: {len(devices)}")
    for device in devices['devices']:
        print(f"device: {device['name']}, active: {device['is_active']}") 

    #start playback of top recommendation song if device is available
    if len(devices) >= 1 and devices['devices'][0]['is_active']:
        sp.start_playback(uris=[uri])
        sp.repeat(state="off")
        sp.shuffle(state=True)
        for track in recommendations[1:]:
            sp.add_to_queue(track['uri'])

        
    else:
        print("No available devices to start playback")









