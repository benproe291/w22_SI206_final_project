import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pprint
import requests

import sqlite3
import json
import os

import matplotlib.pyplot as plt
import plotly.express as pltly


def find_top_songs(off):
    scope = 'user-top-read'
    ranges = ['short_term', 'medium_term', 'long_term']

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    for sp_range in ['medium_term']:
        results = sp.current_user_top_artists(time_range=sp_range, limit=20, offset= off)
        #pprint.pprint(results)

    #pprint.pprint(jsn['items'])
    return results

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
    print(f'fetching top artists from Spotify, offset = {offset}')
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
        #print(artist, genre1, genre2)
    conn.commit()

def find_events(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS venue (venue_id TEXT PRIMARY KEY, venue_name TEXT, venue_lat NUMBER, venue_log NUMBER, city TEXT, state TEXT)')
    conn.commit()
    
    events = []

    artists = cur.execute("SELECT name from top_artists")
    for a in artists:
        name = a[0]
        print(f'retrieving <= 20 event results from Ticketmaster, search term = {a}')
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

def create_venue(cur, conn):
 
    print('please wait... fetching venue list')
    venues = find_events(cur, conn)
    for venue in venues:
        try:
            venue_id = venue['_embedded']['venues'][0]['id']
            venue_name = venue['_embedded']['venues'][0]['name']
            venue_lat = venue['_embedded']['venues'][0]['location']['latitude']
            venue_log = venue['_embedded']['venues'][0]['location']['longitude']
            city = venue['_embedded']['venues'][0]['city']['name']
            state = venue['_embedded']['venues'][0]['state']['name']
            cur.execute("INSERT INTO venue (venue_id, venue_name, venue_lat, venue_log, city, state) VALUES (?,?,?,?,?,?)", (venue_id, venue_name, venue_lat, venue_log, city, state))
            conn.commit()
        except:
            continue



def create_events(cur, conn):
    
    # find events
    print('please wait... fetching event results')
    events = find_events(cur, conn)
    cur.execute('CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, event_name TEXT, genre TEXT, date TEXT, venue_id TEXT)')
    conn.commit()

    for event in events:
        try:
            event_id = event["id"]
            event_name = event["name"]
            genre = event["classifications"][0]["genre"]["name"]
            date = event["dates"]["start"]["localDate"]
            venue_id = event['_embedded']['venues'][0]['id']
            cur.execute("INSERT INTO events (event_id, event_name, genre, date, venue_id) VALUES (?,?,?,?,?)", (event_id, event_name, genre, date, venue_id))
            conn.commit()
        except:
           continue
    print(f"task complete, please view 'top_artists_concerts.db")

def viz_one(cur, conn):
    state_count = cur.execute('''
        SELECT DISTINCT venue.state, count(*) as count
        FROM venue
        JOIN events
        ON venue.venue_id = events.venue_id
        GROUP BY venue.state''').fetchall()
    x_list = []
    y_list = []
    for i in state_count:
        x_list.append(i[0])
        y_list.append(i[1])
    plt.barh(x_list, y_list)
    plt.xlabel('Number of Shows/Events')
    plt.ylabel("State")
    plt.title("Number of Shows/Events by State")
    plt.tight_layout()
    plt.show()

def viz_two(cur, conn):
    genre1_count = cur.execute(
        '''SELECT DISTINCT top_artists.genre1, count(*) as count
           FROM top_artists
           GROUP BY top_artists.genre1'''
    )
    x_list = []
    y_list = []
    for i in genre1_count:
        x_list.append(i[0])
        y_list.append(i[1])
    plt.pie(y_list, labels=x_list)
    plt.title("Pie Chart of the Primary Genre of your Top Artists from the last 6 months")
    plt.show()
    pass


cur, conn = setUpDatabase("attempt2.db")

create_top_artists(cur, conn, 0)
create_top_artists(cur, conn, 20)
create_top_artists(cur, conn, 40)
create_venue(cur, conn)
create_events(cur, conn)
viz_one(cur, conn)
#viz_two(cur, conn)
