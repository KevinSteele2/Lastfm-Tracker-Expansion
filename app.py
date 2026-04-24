from flask import Flask, jsonify, render_template, request
import os
import time
import sys
sys.path.append('.')
from main import get_all_scrobbles, group_by_album, album_play_counts, load_cache, save_cache, fetch_missing_albums

app = Flask(__name__)
scrobble_cache = {}

@app.route('/')
def index():
    return render_template('room.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sq3r')
def sq3r():
    return render_template('sq3r.html')

@app.route('/spotify')
def spotify():
    return render_template('spotify.html')

@app.route('/lastfm')
def lastfm():
    return render_template('lastfm.html')

@app.route('/api/albums')
def get_albums():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Invalid Username"}), 400
    
    if username not in scrobble_cache or time.time() - scrobble_cache[username]['time'] > 3600:
        scrobble_cache[username] = {'tracks': get_all_scrobbles(username), 'time': time.time()}
    tracks = scrobble_cache[username]['tracks']
    albums = group_by_album(tracks)
    cache = load_cache(username)
    fetch_missing_albums(albums, cache)
    save_cache(username, cache)
    play_counts = album_play_counts(albums, cache)
    album_list = []

    for key, count in play_counts.items():
        if count > 0:
            album_list.append({
                "name": key,
                "count": count,
                "cover": cache.get(key, {}).get("cover")
            })

    for i in range(len(album_list)):
        for j in range(i + 1, len(album_list)):
            if album_list[j]["count"] > album_list[i]["count"]:
                album_list[i], album_list[j] = album_list[j], album_list[i]

    return jsonify(album_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))