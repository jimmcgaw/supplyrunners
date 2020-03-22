import requests

from django.conf import settings

PLACES_SEARCH_BASE_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?parameters'

def find_places(search_text, lat=None, long=None, ip_address=None):
    url = PLACES_SEARCH_BASE_URL
    params = {
        'key': settings.GMAP_API_KEY,
        'inputtype': 'textquery',
        'input': search_text,
        'fields': ','.join(['name', 'icon', 'place_id', 'formatted_address', 'geometry'])
    }
    return requests.get(url, params=params).json()