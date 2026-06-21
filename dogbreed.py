import requests
 
WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
 

STARTER_BREEDS = [
    "Labrador Retriever",
    "German Shepherd",
    "Golden Retriever",
    "French Bulldog",
    "Bulldog",
    "Poodle",
    "Beagle",
    "Rottweiler",
    "Dachshund",
    "Siberian Husky",
    "Shih Tzu",
    "Boxer (dog)",       
    "Great Dane",
    "Chihuahua (dog breed)",  
    "Pug",
    "Border Collie",
    "Australian Shepherd",
    "Yorkshire Terrier",
    "Doberman",
    "Corgi",
]
 
 
def get_breed_info(wiki_title):
    """
    Fetch a single breed's summary from Wikipedia.
 
    Returns a dict: {name, image_url, extract, page_url}
    or None if the page has no usable thumbnail.
    """
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
 
 
def test_starter_breeds():
    results = []
    for breed in STARTER_BREEDS:
        info = get_breed_info(breed)
        if info:
            results.append(info)
            print(f"  [ok]   {info['name']} -> {info['image_url']}")
    return results
 
 
if __name__ == "__main__":
    print(f"Testing {len(STARTER_BREEDS)} breeds against Wikipedia REST API...\n")
    results = test_starter_breeds()
    print(f"\n{len(results)}/{len(STARTER_BREEDS)} breeds returned a usable image.")