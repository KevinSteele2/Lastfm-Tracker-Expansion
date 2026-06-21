import random
from difflib import SequenceMatcher

import requests

WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"


COMMON_BREEDS = [
    {"title": "Labrador Retriever", "aliases": ["lab", "labrador"]},
    {"title": "German Shepherd", "aliases": ["gsd", "german shepherd dog"]},
    {"title": "Golden Retriever", "aliases": ["golden"]},
    {"title": "French Bulldog", "aliases": ["frenchie"]},
    {"title": "Bulldog", "aliases": ["english bulldog", "british bulldog"]},
    {"title": "Poodle", "aliases": []},
    {"title": "Beagle", "aliases": []},
    {"title": "Rottweiler", "aliases": ["rottie"]},
    {"title": "Dachshund", "aliases": ["wiener dog", "sausage dog", "doxie"]},
    {"title": "Siberian Husky", "aliases": ["husky"]},
    {"title": "Shih Tzu", "aliases": []},
    {"title": "Boxer (dog)", "aliases": ["boxer"]},
    {"title": "Great Dane", "aliases": []},
    {"title": "Chihuahua (dog breed)", "aliases": ["chihuahua"]},
    {"title": "Pug", "aliases": []},
    {"title": "Border Collie", "aliases": []},
    {"title": "Australian Shepherd", "aliases": ["aussie"]},
    {"title": "Yorkshire Terrier", "aliases": ["yorkie"]},
    {"title": "Dobermann", "aliases": ["doberman", "doberman pinscher"]},
    {"title": "Pembroke Welsh Corgi", "aliases": ["corgi", "welsh corgi"]},
]


def get_breed_info(wiki_title):
    url = WIKI_SUMMARY_URL.format(title=wiki_title.replace(" ", "_"))
    response = requests.get(url, headers={"User-Agent": "DogBreedGame/0.1"})

    if response.status_code != 200:
        print(f"  [skip] {wiki_title}: HTTP {response.status_code}")
        return None

    data = response.json()

    thumbnail = data.get("thumbnail", {})
    image_url = thumbnail.get("source")

    if not image_url:
        print(f"  [skip] {wiki_title}: no thumbnail image")
        return None

    return {
        "name": data.get("title"),
        "image_url": image_url,
        "image_width": thumbnail.get("width"),
        "image_height": thumbnail.get("height"),
        "extract": data.get("extract"),
        "page_url": data.get("content_urls", {}).get("desktop", {}).get("page"),
    }


def _normalize(text):
    return text.lower().strip().replace("-", " ")


def check_guess(breed_id, guess, aliases=None, threshold=0.82):
    aliases = aliases or []
    candidates = [breed_id] + aliases
    guess_norm = _normalize(guess)

    for candidate in candidates:
        score = SequenceMatcher(None, guess_norm, _normalize(candidate)).ratio()
        if score >= threshold:
            return True, breed_id

    return False, breed_id