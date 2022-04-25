import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

import sqlite3
import json
import os

ACCESS_TOKEN = 'BQCK3w5tdw10ad75c5R36Xz0iMqg1bWNFD0i3m4U__QYJj8m6LzyFuq-RKqdfl5H4upWmUBgEk6K6J5mn3RfrHU-Gp2SQrgbJpxXyvy17UFuh03suMkIo070FR_TH30MhgTTfFmOu6Pi0OzIhH4EwD4'
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
    cur.execute('CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, event_name TEXT, genre TEXT, date TEXT, venue TEXT, city TEXT)')
    conn.commit()
    events = []

    artists = cur.execute("SELECT name from top_artists")
    for a in artists:
        name = a[0]

        # filtered data, now data is a list of events
        url = "https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&apikey=F429VW6ixtsWtGtKWzffWwfzDcO9Ad8x".format(name)
        data = requests.get(url).json()

        #pprint.pprint(data)
        try:
            limit_data = data["_embedded"]["events"][:20]
            events += limit_data
        except:
            continue

        
    return events


def create_events(cur, conn):

    # find events
    print('please wait... fetching event results')
    events = find_events(cur, conn)

    for event in events:
        try:
            event_id = event["id"]
            event_name = event["name"]
            genre = event["classifications"][0]["genre"]["name"]
            date = event["dates"]["start"]["localDate"]
            venue_name = event['_embedded']['venues'][0]['name']
            city = event['_embedded']['venues'][0]['city']['name']
            cur.execute("INSERT INTO events (event_id, event_name, genre, date, venue, city) VALUES (?,?,?,?,?,?)", (event_id, event_name, genre, date, venue_name, city))
            conn.commit()
        except:
           continue

cur, conn = setUpDatabase("top_artists_concerts")
create_top_artists(cur, conn, 0)
create_top_artists(cur, conn, 20)
create_top_artists(cur, conn, 40)
create_events(cur, conn)