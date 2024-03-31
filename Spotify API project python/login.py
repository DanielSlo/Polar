

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyPKCE
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import uuid  # Import the UUID module to generate unique IDs for each user
import os
import shutil

import streamlit as st
from datetime import datetime
import time



# Generate a unique identifier for the current user session
user_session_id = str(uuid.uuid4())

SPOTIPY_CLIENT_ID='23a9fab99eee4d3a81a64dcbbe35b546'
SPOTIPY_CLIENT_SECRET='b2eb7cde914b4aaaaec6f4b542378dfa'
SPOTIPY_REDIRECT_URI='http://localhost:3000'

scope = ["user-library-read", "user-modify-playback-state", 
         "user-top-read", "user-read-recently-played", "user-read-playback-state", "user-read-private"]



CACHE_DIR = "caches"
st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
# st.set_page_config(menu_items=None, initial_sidebar_state="collapsed")


st.title("Login to Spotify")
clicked = st.button("Log In")
if clicked:
    #works to require login every time it is a new user
    sp = spotipy.Spotify(auth_manager=SpotifyPKCE(scope=scope, 
                                               client_id=SPOTIPY_CLIENT_ID,  
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               cache_path=os.path.join(CACHE_DIR,f'.spotifycache_{user_session_id}')))
    sp.currently_playing()

    st.session_state['sp'] = sp

    # # Call the 'me' endpoint to get user information
    # sp.current_user()

    #save user info to a global variable (across all pages of the app)
    # st.session_state['user_info'] = user_info
    # # Display user information and image
    # st.sidebar.image(user_info['images'][0]['url'], width=100)
    # st.sidebar.write(f"Currently logged in as: {user_info['display_name']}")



    
    st.switch_page("pages/recommendations.py")
    
    

CACHE_LIFETIME_SECONDS = 43200  # 12 hours
MAX_CACHE_SIZE_BYTES = 1073741824  # 1 GB

def cleanup_cache():
    while True:
        try:
            # Get the current time
            current_time = time.time()

            # Iterate over files in the cache directory
            for filename in os.listdir(CACHE_DIR):
                filepath = os.path.join(CACHE_DIR, filename)

                # Get the modification time of the file
                modification_time = os.path.getmtime(filepath)

                # Check if the file is older than the cache lifetime
                if current_time - modification_time > CACHE_LIFETIME_SECONDS:
                    os.remove(filepath)

            # Check the total size of the cache directory
            total_size = sum(os.path.getsize(os.path.join(CACHE_DIR, f)) for f in os.listdir(CACHE_DIR))
            if total_size > MAX_CACHE_SIZE_BYTES:
                # Delete the oldest cache file
                oldest_file = min(os.listdir(CACHE_DIR), key=lambda f: os.path.getmtime(os.path.join(CACHE_DIR, f)))
                os.remove(os.path.join(CACHE_DIR, oldest_file))
        except FileNotFoundError:
            # Cache directory is empty, continue without deleting files
            pass

        # Sleep for some time before checking again
        # time.sleep(3600)  # Check every hour
        time.sleep(1800)  


# Run the cache cleanup function in a separate thread
import threading
cleanup_thread = threading.Thread(target=cleanup_cache)
cleanup_thread.start()







