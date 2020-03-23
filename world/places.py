import requests

from django.conf import settings


PLACES_SEARCH_BASE_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
PLACE_DETAILS_BASE_URL = 'https://maps.googleapis.com/maps/api/place/details/json'


def find_places(search_text, lat=None, long=None, ip_address=None):
    params = {
        'key': settings.GMAP_API_KEY,
        'inputtype': 'textquery',
        'input': search_text,
        'fields': ','.join(['name', 'place_id', 'formatted_address', 'geometry'])
    }
    return requests.get(PLACES_SEARCH_BASE_URL, params=params).json()


def get_place_details(place_id):
    params = {
        'key': settings.GMAP_API_KEY,
        'place_id': place_id
    }
    return requests.get(PLACE_DETAILS_BASE_URL, params=params)