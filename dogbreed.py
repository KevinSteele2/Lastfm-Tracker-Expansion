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
    {"title": "Akita (dog)", "aliases": ["akita"]},
    {"title": "Alaskan Malamute", "aliases": ["malamute"]},
    {"title": "American Bulldog", "aliases": []},
    {"title": "American Staffordshire Terrier", "aliases": ["amstaff"]},
    {"title": "Basenji", "aliases": []},
    {"title": "Basset Hound", "aliases": []},
    {"title": "Bearded Collie", "aliases": []},
    {"title": "Belgian Malinois", "aliases": ["malinois"]},
    {"title": "Bernese Mountain Dog", "aliases": ["berner"]},
    {"title": "Bichon Frise", "aliases": ["bichon"]},
    {"title": "Bloodhound", "aliases": []},
    {"title": "Bull Terrier", "aliases": []},
    {"title": "Bullmastiff", "aliases": []},
    {"title": "Cairn Terrier", "aliases": []},
    {"title": "Cane Corso", "aliases": []},
    {"title": "Cavalier King Charles Spaniel", "aliases": ["cavalier"]},
    {"title": "Chinese Shar-Pei", "aliases": ["shar pei"]},
    {"title": "Chow Chow", "aliases": []},
    {"title": "Cocker Spaniel", "aliases": []},
    {"title": "Collie", "aliases": ["rough collie"]},
    {"title": "Dalmatian dog", "aliases": ["dalmation"]},
    {"title": "English Mastiff", "aliases": ["mastiff"]},
    {"title": "English Setter", "aliases": []},
    {"title": "English Springer Spaniel", "aliases": ["springer spaniel"]},
    {"title": "Field Spaniel", "aliases": []},
    {"title": "Flat-coated Retriever", "aliases": []},
    {"title": "Fox Terrier", "aliases": []},
    {"title": "German Shorthaired Pointer", "aliases": ["gsp"]},
    {"title": "Great Pyrenees", "aliases": []},
    {"title": "Greyhound", "aliases": []},
    {"title": "Havanese", "aliases": []},
    {"title": "Irish Setter", "aliases": []},
    {"title": "Irish Wolfhound", "aliases": []},
    {"title": "Italian Greyhound", "aliases": []},
    {"title": "Jack Russell Terrier", "aliases": []},
    {"title": "Japanese Chin", "aliases": []},
    {"title": "Keeshond", "aliases": []},
    {"title": "Lhasa Apso", "aliases": []},
    {"title": "Maltese dog", "aliases": ["maltese"]},
    {"title": "Mastiff", "aliases": []},
    {"title": "Miniature Pinscher", "aliases": ["min pin"]},
    {"title": "Miniature Schnauzer", "aliases": ["schnauzer"]},
    {"title": "Newfoundland dog", "aliases": ["newfoundland"]},
    {"title": "Norwegian Elkhound", "aliases": []},
    {"title": "Old English Sheepdog", "aliases": []},
    {"title": "Papillon dog", "aliases": ["papillon"]},
    {"title": "Pekingese", "aliases": []},
    {"title": "Pointer (dog breed)", "aliases": ["english pointer"]},
    {"title": "Pomeranian dog", "aliases": ["pomeranian"]},
    {"title": "Portuguese Water Dog", "aliases": []},
    {"title": "Pug", "aliases": []},
    {"title": "Rhodesian Ridgeback", "aliases": []},
    {"title": "Saint Bernard (dog)", "aliases": ["st bernard", "saint bernard"]},
    {"title": "Samoyed dog", "aliases": ["samoyed"]},
    {"title": "Schipperke", "aliases": []},
    {"title": "Scottish Terrier", "aliases": ["scottie"]},
    {"title": "Shetland Sheepdog", "aliases": ["sheltie"]},
    {"title": "Shiba Inu", "aliases": []},
    {"title": "Shih Tzu", "aliases": []},
    {"title": "Soft-coated Wheaten Terrier", "aliases": ["wheaten terrier"]},
    {"title": "Staffordshire Bull Terrier", "aliases": ["staffy"]},
    {"title": "Standard Schnauzer", "aliases": []},
    {"title": "Vizsla", "aliases": []},
    {"title": "Weimaraner", "aliases": []},
    {"title": "West Highland White Terrier", "aliases": ["westie"]},
    {"title": "Whippet", "aliases": []},
    {"title": "American Pit Bull Terrier", "aliases": ["pitbull", "pit bull"]}
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

if __name__ == "__main__":
    import time

    failed = []
    for breed in COMMON_BREEDS:
        info = get_breed_info(breed["title"])
        if not info:
            failed.append(breed["title"])
        time.sleep(1.0)

    print(f"\n{len(COMMON_BREEDS) - len(failed)}/{len(COMMON_BREEDS)} breeds OK\n")
    if failed:
        print("These failed and should be removed from COMMON_BREEDS:")
        for title in failed:
            print(f"  - {title}")