import requests

# to get by genre
genre = "rap"

# to get by artist name
artist = "21 Savage"

# filter by location (country)
countryCode = "US"


# filtered data, now data is a list of events
url = "https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&classificatioName={}&countryCode={}&apikey=F429VW6ixtsWtGtKWzffWwfzDcO9Ad8x".format(artist, genre, countryCode)
data = requests.get(url).json()
data = data["_embedded"]["events"]
# print(data)

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
