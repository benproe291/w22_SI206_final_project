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
print(data)


