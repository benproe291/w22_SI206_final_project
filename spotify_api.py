import requests
import pprint

ACCESS_TOKEN = 'BQBZMXhuGFfU9RZC2Y8JfE41i6CZj5dRXh4dwQCjYdx_19uZnBOxrWRSjX5tgZuOQkRqVDzbLfS4C_oYbHroxBHsRjTv-kdXsUX0fT8_PXTKwAdutVc3UmZ29tSzCFnjxflaRDxd3CajGXVNbdqkFcc'

def find_top_songs():
    response = requests.post(
        headers = {
            "Authorization": f'Bearer {ACCESS_TOKEN}'
        },
        json = {
            "type" : "artists",
            "time_range": "medium_term",
            "limit": "20"
        }
    )
    json_resp = response.json()
    print(json_resp)
    return json_resp
