
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

scope = ["user-library-read", "user-modify-playback-state", 
         "user-top-read", "user-read-recently-played", "user-read-playback-state"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def get_recommendations(track_name):
    # Get track URI
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
    else:
        print("No available devices to start playback")









