import requests
import pprint

ACCESS_TOKEN = 'BQAeeZCv5wGKFjjbxLwC44wE4qSjWSIFTdjeS4oIhajyqcI3YUVHjSmbZKzFTfhyZEGdImoRQQsQr9dzI0_-S1ppMZ9IJ484ansqmAV1Gik8xqvBDbnIWnIoHAGv2X20N0xR1_37A0hiJVpfcFO8gLE'
root_url = "https://api.spotify.com/v1/me/top/"

def find_top_songs():
    response = requests.post(
        root_url,
        headers = {
            "Authorization": f'Bearer {ACCESS_TOKEN}'
        },
        json = {
            "type" : "artists",
            "time_range": "medium_term",
            "limit": "1"
        }
    )
    json_resp = response.json()
    print(json_resp)

find_top_songs()

