# TO activate venv type lastfm/Scripts/activate in terminal
import requests
API_KEY = "0472b186832ba248f24acf8f554113df"
API_SECRET = "572a702051f64a54b75d8a3f552f1437"
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
