# TO activate venv type lastfm/Scripts/activate in terminal
import requests
from dotenv import load_dotenv
import os

load_dotenv("lastfm/.env")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USERNAME = "Donaldddddd"

def test_user_info():
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getinfo",
        "user": USERNAME,
        "api_key": API_KEY,
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Username: {data['user']['name']}")
    print(f"Scrobbles: {data['user']['playcount']}")
    return response.json()

def test_recent_tracks():
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": USERNAME,
        "api_key": API_KEY,
        "limit": 10,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    tracks = data['recenttracks']['track']
    print(f"\nRecent Tracks Status Code: {response.status_code}")
    for i, track in enumerate(tracks, 1):
        print(f"\n{i}. {track['name']}")
        print(f"    Artist: {track['artist']['#text']}")
        print(f"    Album: {track['album']['#text']}")
        print(f"    Date: {track['date']['#text']}")
    return response.json()

if __name__ == "__main__":
    test_user_info()
    test_recent_tracks()
