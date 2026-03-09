from flask import Flask, jsonify, render_template, request
import sys
sys.path.append('.')
from main import get_all_scrobbles, group_by_album, album_play_counts, load_cache, save_cache, fetch_missing_albums

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/albums')
def get_albums():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Invalid Username"}), 400
    tracks = get_all_scrobbles(username)
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
    app.run(debug=True)