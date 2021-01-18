import requests
from bs4 import BeautifulSoup
import spotipy as sp

id = "c1c7335fdf0c43a7b958407bcd401010" #id с secret-ом были создани в учебных целях, я не лошара
secret = "96e640548aa44c3c8f9434af2d62253b"
data = input("input billboard data for top 100 musics in that week (YYYY-MM-DD) ")
red_uri = "http://example.com"
url = f"https://www.billboard.com/charts/hot-100/{data}"

req = requests.get(url)

soup = BeautifulSoup(req.text, "html.parser")

titles = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")

titles_texted = [title.getText() for title in titles]

ids = []
auth = sp.Spotify(
    auth_manager = sp.SpotifyOAuth(
        client_id=id,
        client_secret=secret,
        redirect_uri=red_uri,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="cache.txt"
    )
)
username = auth.current_user()["id"]
for i in titles_texted:
    try:
        id = auth.search(q=f'track:{i} "year:{data.split("-")[0]}"', type="track")['tracks']["items"][0]["uri"]
        ids.append(id)
    except IndexError:
        print(f"{i} doesn't exist in spotify database")
playlist = auth.user_playlist_create(user=username, name=f"Go back to {data}", public=False, description="Top 100 songs")
playlist_id = playlist["id"]
auth.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=ids)