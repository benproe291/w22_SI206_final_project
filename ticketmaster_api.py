import requests
import sqlite3
import json
import os

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, event_name TEXT, genre TEXT, date TEXT)')
    conn.commit()
    return cur, conn


def find_events(artist, genre="", countryCode="US"):
    # filtered data, now data is a list of events
    url = "https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&classificatioName={}&countryCode={}&apikey=F429VW6ixtsWtGtKWzffWwfzDcO9Ad8x".format(artist, genre, countryCode)
    data = requests.get(url).json()
    data = data["_embedded"]["events"]
    return data


def create_events(cur, conn, artist, genre="", countryCode="US"):

    # find events
    events = find_events(artist)

    for event in events:
        event_id = event["id"]
        event_name = event["name"]
        genre = event["classifications"][0]["genre"]["name"]
        date = event["dates"]["start"]["localDate"]
        cur.execute("INSERT INTO events (event_id, event_name, genre, date) VALUES (?,?,?,?)", (event_id, event_name, genre, date))

    conn.commit()


cur, conn = setUpDatabase("top_artists_concerts")
artist = "Dababy"
create_events(cur, conn, artist)



### -- MAKE SURE TO HIT -- # (300 points)
# Get at least 100 rows (have multiple calls to multiple favorite artists)
# Artist Table / Genre Table (shared key is genre key?)
# make sure to add at most 20 rows per call (can do multiple calls & limit)

# Calculate some kind of average (count of each genre / favorite artist)
# We can use "JOIN" in connecting artists/genre's (can search on both)
# write to file

# make 2 visualizations (fav artist/genre pie chart), hot spots of concerts (can filter by state or somethign)

# Report: problems/goals (30 points), include files, directions, and visualizations (30 point),
# make sure that code is documented / resources are documented (40 points)
