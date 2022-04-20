import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint


ACCESS_TOKEN = 'BQAYvAdy7wtzIwjFHOl63mrfdPVEGdOnCZ70P_G3oCRo_IafmmZGR5s77qGup76KXje0IlAgJ5Trw-ipIWGhnjkoPotasMIukg5yJhuqssSsI56hH9MIn2DWgjqaAHLcYqZf06L-RzlEUU09h7S4tKY'
root_url = "https://api.spotify.com/v1/me/top/artists?"

def find_top_songs():
    tr = "medium_term"
    lm = "4"
    offset = '0'
    response = requests.get(
        f'https://api.spotify.com/v1/me/top/artists?time_range={tr}&limit={lm}&offset={offset}',
        headers = {
            "Accept": f'application/json',
            "Content-Type": f'application/json',
            "Authorization": f'Bearer {ACCESS_TOKEN}'
        }
    )
    jsn = response.json()
    pprint.pprint(jsn)
    return jsn
find_top_songs()

