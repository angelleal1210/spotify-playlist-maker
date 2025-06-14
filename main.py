import sys
import json
import requests
from bs4 import BeautifulSoup
import pprint
username = "31wtohyn3sx75oc6l3i2efxtp6b4"
client_id = "42fa8c20c7b74f918bc0efdeaefb7dea"
client_secret= "cant share publicly"
redirect_url = "http://127.0.0.1:8080/"
scope = "playlist-modify-public"
url = "https://www.billboard.com/charts/hot-100/"
print("Welcome to the spotify time machine")
date = input("Type the date in this format yyyy-mm-dd: ")
final_link = url+date
response = requests.get(final_link)
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
song_names = [song.getText() for song in songs]
songs_1 = [song.replace("\n", "") for song in song_names]
songs_final = [song.replace("\t", "") for song in songs_1]
import spotipy
from spotipy.oauth2 import SpotifyOAuth
token = SpotifyOAuth(scope=scope, username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url)
spotifyObject = spotipy.Spotify(auth_manager=token)
#create the playlist
playlist_name = F"{date}"
description = "top 100"
spotifyObject.user_playlist_create(username, name=playlist_name, description=description)
songs_to_add=[]
for song in songs_final:
    result = spotifyObject.search(q=song)
    uri = result['tracks']['items'][0]['uri']
    songs_to_add.append(uri)
pre = spotifyObject.user_playlists(user=username)
playlist = pre['items'][0]['id']
spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=songs_to_add)


