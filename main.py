from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
import spotipy

SPOTIPY_CLIENT_ID = 'c8057aa235384c71b85c8ef26ec10d37'
SPOTIPY_CLIENT_SECRET = 'eb61fd3563ee4fd1a26d780c37817c0f'
SPOTIPY_REDIRECT_URI = 'http://example.com'

user = 'oxy2m0nxdc7gz7cnmd8c5xl93'
URL = 'https://www.billboard.com/charts/hot-100/'
# token = {"access_token": "BQB7AU9nKGrwwjiza4gDtnOLSxDcRyAfVlua6tpCNOVZWA_Zm5HPIPiLm1nipLo0HWHdNTYbLO49sTKCzRSh4JII1qGLtHqLhEh7np4OQeP1aPdDtCTLasx5PDDSZ5vQmrfBm7XBVcyeht1KmrNCH_wdg8E_QcYK5uaB4X4FHMwZ4r6EWMmagi0lGPAM-Ns54HbjzHAwDwGSn8U",
#         "token_type": "Bearer", "expires_in": 3600, "scope": null, "expires_at": 1688328968, "refresh_token": "AQDAGj_g-qoGAtGVKCNMlvZck8zxQwgYOTx7phyrq2mwuEpVHUVzKpKiUzxHNupMQp3OyZgjmuzNmu1m3H5W66-QsfeUpx_jKVuRui5VUrLpBnA69CpAAmlavX_XZbk8qeE"}


time_machine = input('Which year do you want to travel to (YYYY-MM-DD)? ')

response = requests.get(URL + time_machine+'/')
billboard = response.text


soup = BeautifulSoup(billboard, "html.parser")
top100 = soup.select("li ul li h3")

bilboard100 = [n.getText().strip() for n in top100]


scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=".cache.json",
    username='Yahya'))


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
