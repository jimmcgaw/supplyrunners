from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.shortcuts import render

from .places import find_places

# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def feedback(request):
    return render(request, 'feedback.html')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


@login_required
def account_settings(request):
    return render(request, 'settings.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def locations(request):
    # raise Exception(dir(request.user))
    # raise Exception(dir(request.user.social_auth))
    # raise Exception(request.user.id)
    return render(request, 'locations.html', {'map_key': settings.GMAP_API_KEY})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def locations_search(request):
    if not request.GET.get('q'):
        return JsonResponse({})

    lat = request.GET.get('lat')
    long = request.GET.get('long')
    ip_address = get_client_ip(request)
    places_json = find_places(request.GET.get('q'), lat=lat, long=long, ip_address=ip_address)
    return JsonResponse(places_json)