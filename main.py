from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
import spotipy
import config


URL = 'https://www.billboard.com/charts/hot-100/'


time_machine = input('Which year do you want to travel to (YYYY-MM-DD)? ')

response = requests.get(URL + time_machine+'/')
billboard = response.text


soup = BeautifulSoup(billboard, "html.parser")
top100 = soup.select("li ul li h3")

bilboard100 = [n.getText().strip() for n in top100]


scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    config.SPOTIPY_CLIENT_ID, config.SPOTIPY_CLIENT_SECRET, config.SPOTIPY_REDIRECT_URI, scope=scope, cache_path=".cache.py",
    username='oxy2m0nxdc7gz7cnmd8c5xl93'))


song_uris = []
year = time_machine.split("-")[0]
for song in bilboard100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    sp.current_user()['id'], "Billboard Top 100 "+time_machine, public=False, collaborative=False, description='Contains billboards top 100 from '+time_machine)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
