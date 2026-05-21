import requests

def get_nearby_hotels(lat, lon):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": 2000,
        "type": "lodging",
        "key": "YOUR_GOOGLE_API_KEY"
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])
