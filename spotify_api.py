import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

import sqlite3
import json
import os

ACCESS_TOKEN = 'BQDA8IxmLAL5Q6ZXiY2aYPr7p_fbJ0iBtDwYrcqZpB0_plFe9J-DlgSit2Zl1MlvBwkvMgy6NlALXmdRwAo7ri92jxOnP6Mo7V_GVJlNbOVK0V4CFq6yJ0GY4fj1uH119oaGYtv3fsqwnUzIZP2uUVM'
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
    #cur.execute("DROP TABLE IF EXISTS top_artists")
    #conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS top_artists (artist_id INTEGER PRIMARY KEY, name TEXT, genre1 TEXT, genre2 TEXT)')
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

def find_events(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, event_name TEXT, genre TEXT, date TEXT)')
    conn.commit()
    events = []

    artists = cur.execute("SELECT name from top_artists")
    for a in artists:
        name = a[0]

        # filtered data, now data is a list of events
        url = "https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&apikey=F429VW6ixtsWtGtKWzffWwfzDcO9Ad8x".format(name)
        data = requests.get(url).json()
        data = data["_embedded"]["events"]
        events += data

    return events


def create_events(cur, conn):

    # find events
    events = find_events(cur, conn)

    for event in events:
        event_id = event["id"]
        event_name = event["name"]
        genre = event["classifications"][0]["genre"]["name"]
        date = event["dates"]["start"]["localDate"]
        cur.execute("INSERT INTO events (event_id, event_name, genre, date) VALUES (?,?,?,?)", (event_id, event_name, genre, date))

    conn.commit()


cur, conn = setUpDatabase("top_artists_concerts")
create_events(cur, conn)


cur, conn = setUpDatabase("top_artists_concerts")
create_top_artists(cur, conn, 0)
create_top_artists(cur, conn, 20)
create_top_artists(cur, conn, 40)
