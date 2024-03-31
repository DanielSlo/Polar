

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyPKCE
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import uuid  # Import the UUID module to generate unique IDs for each user
import os
import shutil
import threading
import hashlib

import streamlit as st
from datetime import datetime
import time

import cacheFunctions

#hide sidebar
st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)



with open('login_flag.txt', 'w') as f:
        f.write('')


# Generate a unique identifier for the current user session
# user_session_id = str(uuid.uuid4())
# def generate_session_id(username):
#     # Generate a unique session ID based on the user's username
#     return hashlib.sha256(username.encode()).hexdigest()


# Function to generate or retrieve a unique user identifier
def get_or_set_user_id():
    user_id = st.session_state.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())  # Generate a new user ID
        st.session_state.user_id = user_id  # Store user ID in session state
    return user_id

SPOTIPY_CLIENT_ID='23a9fab99eee4d3a81a64dcbbe35b546'
SPOTIPY_CLIENT_SECRET='b2eb7cde914b4aaaaec6f4b542378dfa'
SPOTIPY_REDIRECT_URI='http://localhost:3000'

scope = ["user-library-read", "user-modify-playback-state", 
         "user-top-read", "user-read-recently-played", "user-read-playback-state", "user-read-private"]




# st.set_page_config(menu_items=None, initial_sidebar_state="collapsed")

CACHE_DIR = "caches"
st.title("Login to Spotify")
clicked = st.button("Log In")
if clicked:
    user_id = get_or_set_user_id()
    #works to require login every time it is a new user
    sp = spotipy.Spotify(auth_manager=SpotifyPKCE(scope=scope, 
                                               client_id=SPOTIPY_CLIENT_ID,  
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               cache_path=os.path.join(CACHE_DIR,f'.spotifycache_{user_id}')))
    

    #calls sp object, prompts user to login and accept scopes
    sp.currently_playing()

    # Run the cache duplicate remover function in a separate thread    
    remove_cache_duplicates = threading.Thread(target=cacheFunctions.remove_duplicates)
    remove_cache_duplicates.start()
    st.session_state['sp'] = sp
    


    # st.session_state.logged_in = True

    #will use as a flag to avoid recommendations.py from running until login is complete, will store value in login_flag.txt
    def update_session_state(value):
        with open('login_flag.txt', 'w') as f:
            f.write(str(value))

    #  Successful login process
    # Update session state to indicate that the user is logged in
    update_session_state(True)

    #redirect to recommendations.py or any other page
    st.switch_page("pages/recommendations.py")
    
    



# Run the cache cleanup function in a separate thread
cleanup_thread = threading.Thread(target=cacheFunctions.cleanup_cache)
cleanup_thread.start()







