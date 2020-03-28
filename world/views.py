from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.shortcuts import render, redirect

from django.urls import reverse

from .forms import UserProfileForm
from .models import UserProfile, UserLocation
from .places import find_places, get_place_details


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def feedback(request):
    return render(request, 'feedback.html')


def resources(request):
    return render(request, 'resources.html')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


@login_required
def account_settings(request):
    return render(request, 'settings.html')


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.kind:
        return redirect(reverse('profile_edit'))
    return render(request, 'profile.html')


def _get_user_social_name(user):
    return user.social_auth.extra()[0].extra_data['name']


def _get_user_social_email(user):
    return user.social_auth.extra()[0].extra_data['email']


@login_required
def profile_edit(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        data = request.POST.copy()
        form = UserProfileForm(data, instance=user_profile)

        if form.is_valid():
            form.save()
            if not request.user.locations.all():
                # if user hasn't set any locations, nudge them
                return redirect(reverse('locations'))
            return redirect(reverse('profile'))
    else:
        initial_data = {}
        if not user_profile.display_name:
            initial_data['display_name'] = _get_user_social_name(request.user)
        if not user_profile.contact_details:
            initial_data['contact_details'] = _get_user_social_email(request.user)

        form = UserProfileForm(instance=user_profile, initial=initial_data)
    return render(request, 'profile_edit.html', {'form': form})


def _location_data(place_id):
    return get_place_details(place_id)


def _get_location_data(place_ids):
    return {
        'locations': [i for i in map(_location_data, place_ids)]
    }


@login_required
def locations(request):
    if request.is_ajax():
        if request.method == 'POST':
            place_id = request.POST.get('place_id')
            request.user.locations.get_or_create(google_place_id=place_id, user=request.user)
        location_place_ids = [location.google_place_id for location in request.user.locations.all()]
        location_data = _get_location_data(location_place_ids)
        return JsonResponse(location_data)

    return render(request, 'locations.html')



@login_required
def locations_search(request):
    if not request.GET.get('q'):
        return JsonResponse({})

    lat = request.GET.get('latitude')
    long = request.GET.get('longitude')
    places_json = find_places(request.GET.get('q'), lat=lat, long=long)
    return JsonResponse(places_json)