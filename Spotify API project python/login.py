

import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
# Set the port for Streamlit to 3000
PORT = 3000
# st.set_option('server.port', PORT)


client_id = '23a9fab99eee4d3a81a64dcbbe35b546'
client_secret = 'b2eb7cde914b4aaaaec6f4b542378dfa'

clicked = st.button("Click me")

if clicked:
    # Set up the SpotifyOAuth object
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://localhost:8502',  # Your redirect URI
        scope='playlist-modify-public',  # The scopes you need
        cache_path='.spotifycache'  # Path to a file to store tokens
    )

    # Get the authorization URL
    auth_url = sp_oauth.get_authorize_url()

    # Display the authorization URL in the Streamlit app
    st.write("Please visit the following URL to authorize your account:")
    st.write(auth_url)





