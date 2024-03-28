import os
import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth




#user defined functions
import recommendations 

scope = ["user-library-read", "user-modify-playback-state", 
         "user-top-read", "user-read-recently-played", "user-read-playback-state"]



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_top_tracks(limit = 5)

#get nicer output to see what is inside dictionary
# print(json.dumps(results, sort_keys=False, indent=4))

#print user's top 5 songs
print("Your top songs:")
counter = 1

top_songs_uri_list = []
for track in results['items']:
    print(f"{counter}. {track['name']}")
    top_songs_uri_list.append(track['uri'])
    counter += 1
# print(f"URI LIST: {top_songs_uri_list}")

#get URI of #1 top song
uri = results['items'][0]['uri']
# print(f"uri is {uri}")

#get available devices
devices = sp.devices()
#full print of devices response
# print(json.dumps(devices, sort_keys=False, indent=4))

#print available devices and their status
print(f"\n\nnum devices: {len(devices)}")
for device in devices['devices']:
    print(f"device: {device['name']}, active: {device['is_active']}") 




#start playback of top song if 
if len(devices) >= 1 and devices['devices'][0]['is_active']:
    sp.start_playback(uris=[uri])
else:
    print("No available devices to start playback")

# for idx, item in enumerate(results['items']):
#     print(item['name'])

#get recommendations based on a single song
recs = recommendations.get_recommendations("mwaki")
# print(json.dumps(res, sort_keys=False, indent=4))
print(f"single song rec: {recs[1]['name']}")


# recsmult = recommendations.get_recommendations_multiple_songs(combined_string)

#print recommendations based on input song
print("\n\nrecommendations based on your top songs")
counter = 1
for rec in recs:
    print(f"{counter}. {rec['name']}")
    counter += 1
print()