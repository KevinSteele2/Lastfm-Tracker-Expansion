from flask import Flask, jsonify, render_template
import sys
sys.path.append('.')
from main import get_all_scrobbles, group_by_album, album_play_counts, album_track_count, load_track_count_cache, save_track_count_cache, USERNAME

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/albums')
def get_albums():
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
        album_list.append({"name": key, "count": count})

    #sorting
    for i in range(len(album_list)):
        for j in range(i + 1, len(album_list)):
            if album_list[j]["count"] > album_list[i]["count"]:
                album_list[i], album_list[j] = album_list[j], album_list[i]
    
    return jsonify(album_list[:10])

if __name__ == '__main__':
    app.run(debug=True)