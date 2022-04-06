import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


ACCESS_TOKEN = 'BQCe3M8bGIQZQ0DJnFB8FZpP-uLxRYfncOy7MaOM72-rQ-5gscYT7ySvs_4lz_n4TLfkCSztjF_HGKE68c5taTRNpAUVz_lLIv-U1QJccnE4P2wWVI8IEgjX8Kkm8s50A6XIG44isTp90Wj-1-hQxes'
root_url = "https://api.spotify.com/v1/me/top/artists"

def find_top_songs():
    response = requests.post(
        root_url,
        headers = {
            "Authorization": f'Bearer {ACCESS_TOKEN}'
        },
        json = {
            "time_range": "medium_term",
            "limit": "1",
            "offset": '0'
        }
    )
    json_resp = response
    print(json_resp)

find_top_songs()

