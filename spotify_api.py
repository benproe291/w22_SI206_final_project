import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

import sqlite3
import json
import os

ACCESS_TOKEN = 'BQCvEyNAX4WwnDf1W5j1SSKQHiTJmH8eHREyH1VOX2cX1rLzJRZxhDqrcUHPO8no4QN1A6zak-dP5SFWkl8u5TOpkju48saQ4C2lT830OMDEQPJKzdImz_KB6kbO8mtC3Fx3k8eK_2ToQDwGQRWl5Ok'
root_url = "https://api.spotify.com/v1/me/top/artists?"

def find_top_songs(offset):
    tr = "medium_term"
    lm = "20"
    response = requests.get(
        f'https://api.spotify.com/v1/me/top/artists?time_range={tr}&limit={lm}&offset={offset}',
        headers = {
            "Accept": f'application/json',
            "Content-Type": f'application/json',
            "Authorization": f'Bearer {ACCESS_TOKEN}'
        }
    )
    jsn = response.json()
    #pprint.pprint(jsn['items'])
    return jsn

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_top_artists(cur, conn, offset):
    cur.execute('CREATE TABLE top_artists (artist_id INTEGER PRIMARY KEY, name TEXT, genre1 TEXT, genre2 TEXT)')
    conn.commit()
    data = find_top_songs(offset)
    pprint.pprint(data['items'])
    artist_id = 1
    for item in data['items']:
        artist_id += 1
        artist = item['name']
        try:
            genre1 = item['genres'][0]
        except:
            continue
        try:
            genre2 = item['genres'][1]
        except:
            genre2 = "null"
        cur.execute("INSERT INTO top_artists (name, genre1, genre2) VALUES (?,?,?)", (artist, genre1, genre2))
        print(artist, genre1, genre2)
    conn.commit()


cur, conn = setUpDatabase("top_artists_concerts")
create_top_artists(cur, conn, 0)
create_top_artists(cur, conn, 20)
create_top_artists(cur, conn, 40)
#create_top_artists(cur, conn, 60)
#create_top_artists(cur, conn, 800)