from flask import Flask, jsonify, render_template, request
import os
import time
import sys
sys.path.append('.')
from main import get_all_scrobbles, group_by_album, album_play_counts, load_cache, save_cache, fetch_missing_albums
import dogbreed
import random

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

@app.route('/dogguesser')
def dogbreed_page():
    return render_template('dogbreed.html')

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

@app.route('/api/dogbreed/random')
def dogbreed_random():
    cache = dogbreed.load_cache()
    if not cache:
        return jsonify({"error": "Cache is empty. Run dogbreed.py first to build it."}), 500

    title = random.choice(list(cache.keys()))
    info = cache[title]
    breed = next(b for b in dogbreed.COMMON_BREEDS if b["title"] == title)

    return jsonify({
        "breed_id": title,
        "image_url": info["image_url"],
        "aliases": breed["aliases"]
    })

@app.route('/api/dogbreed/guess', methods=['POST'])
def dogbreed_guess():
    data = request.get_json()
    if not data or 'breed_id' not in data or 'guess' not in data:
        return jsonify({"error": "Request must include breed_id and guess"}), 400

    breed_id = data['breed_id']
    guess = data['guess']
    aliases = data.get('aliases', [])

    correct, answer = dogbreed.check_guess(breed_id, guess, aliases)

    return jsonify({"correct": correct, "answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))