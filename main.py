# TO activate venv type lastfm/Scripts/activate in terminal
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv("lastfm/.env")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USERNAME = "xoforever69"

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

def get_all_scrobbles():
    url = "http://ws.audioscrobbler.com/2.0/"
    all_tracks = []
    page=1
    while True:
        params = {
            "method": "user.getrecenttracks",
            "user": USERNAME,
            "api_key": API_KEY,
            "limit": 200,
            "page": page,
            "format": "json"
        }

        response = requests.get(url, params=params)
        data = response.json()
        tracks = data.get("recenttracks", {}).get("track", [])
        if not isinstance(tracks, list):
            tracks = [tracks]
        
        all_tracks.extend(tracks)

        total_pages = int(data.get("recenttracks", {}).get("@attr", {}).get("totalPages", 1))
        print(f"Fetched page {page} of {total_pages}")
        if page >= total_pages:
            break
        page += 1
    return all_tracks

def group_by_album(tracks):
    albums = {}
    for track in tracks:
        album_name = track.get("album", {})
        if isinstance(album_name, dict):
            album_name = album_name.get("#text", "Unknown")
        
        artist_name = track.get("artist", {})
        if isinstance(artist_name, dict):
            artist_name = artist_name.get("#text", "Unknown")
        
        album_key = f"{album_name} - {artist_name}"

        if album_key not in albums:
            albums[album_key] = {
                "tracks": [],
                "artist": artist_name,
                "album": album_name,
                "cover_art": None
            }
        
        albums[album_key]["tracks"].append(track)

    #fetching cover art
    #for album_key, album_data in albums.items():
        #cover_art = get_album_cover(album_data["album"], album_data["artist"])
        #album_data["cover_art"] = cover_art

    return albums

def get_album_cover(album_name, artist_name):
    url="http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "album.getinfo",
        "artist": artist_name,
        "album": album_name,
        "api_key": API_KEY,
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()
    images = data.get("album", {}).get("image", [])
    if images:
        return images[-1].get("#text", None)

    return None

def album_track_count(album_name, artist_name):
    url="http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "album.getinfo",
        "artist": artist_name,
        "album": album_name,
        "api_key": API_KEY,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    tracks = data.get("album", {}).get("tracks", {}).get("track", [])
    if isinstance(tracks, dict):
        return 1
    return len(tracks)

def full_listen_albums(albums):
    result = {}
    for key, info in albums.items():
        seen = {t.get("name", "").strip() for t in info["tracks"]}
        total = album_track_count(info["album"], info["artist"])
        if total and len(seen) >= total:
            result[key] = info
    return result

def count_full_plays(album_tracks, total_tracks):
    track_counts = {}
    for t in album_tracks:
        name = t.get("name", "").strip()
        if name:
            track_counts[name] = track_counts.get(name, 0) + 1
    
    if len(track_counts) < total_tracks:
        return 0
    
    return min(track_counts.values())

def album_play_counts(albums, track_counts):
    counts = {}
    for key, info in albums.items():
        total = track_counts.get(key, 0)
        if total <= 0:
            continue
        counts[key] = count_full_plays(info["tracks"], total)
    return counts

def load_track_count_cache(username):
    try:
        with open(f"track_counts_{username}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_track_count_cache(username, cache):
    with open(f"track_counts_{username}.json", "w") as f:
        json.dump(cache, f)

if __name__ == "__main__":
    #test_user_info()
    #test_recent_tracks()
    tracks = get_all_scrobbles()
    albums = group_by_album(tracks)

    cache = load_track_count_cache(USERNAME)
    for key, info in albums.items():
        if key not in cache:
            cache[key] = album_track_count(info["album"], info["artist"])
            print(f"Fetched: {key}")
    save_track_count_cache(USERNAME, cache)
    track_counts = cache

    play_counts = album_play_counts(albums, track_counts)

    results = {}
    for key, count in play_counts.items():
        if count > 0:
            results[key] = count
    
    album_list = []
    for key, count in results.items():
        album_list.append((key, count))

    #sorting
    for i in range(len(album_list)):
        for j in range(i + 1, len(album_list)):
            if album_list[j][1] > album_list[i][1]:
                album_list[i], album_list[j] = album_list[j], album_list[i]
    
    top_10 = album_list[:10]

    print(f"\nTop Ten Most Listened Albums:")
    print("-" * 60)
    rank = 1
    for album_key, count in top_10:
        print(f"{rank}. {album_key}: {count} complete listens")
        rank += 1
    