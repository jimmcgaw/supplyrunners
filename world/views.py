from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
    user_profile = request.user.profile
    if not user_profile.kind:
        return redirect(reverse('profile_edit'))

    location_count = request.user.locations.count()

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'location_count': location_count
    })


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
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile_edit.html', {'form': form})


def _location_data(place_id):
    details = get_place_details(place_id)
    return {
        'name': details['result']['name'],
        'address': details['result']['formatted_address'],
        'place_id': place_id
    }


def _get_location_data(place_ids):
    return {
        'locations': [i for i in map(_location_data, place_ids)]
    }


@login_required
def locations(request):
    if request.is_ajax():
        if request.method == 'POST':
            # constrain at 15, fail silently if user is trying to add more than this.
            if request.user.locations.count() < 15:
                place_id = request.POST.get('place_id')
                request.user.locations.get_or_create(google_place_id=place_id, user=request.user)
        location_place_ids = [location.google_place_id for location in request.user.locations.all()]
        location_data = _get_location_data(location_place_ids)
        return JsonResponse(location_data)

    return render(request, 'locations.html')


@login_required
def locations_delete(request):
    if request.is_ajax() and request.method == 'POST':
        place_id = request.POST.get('place_id')
        try:
            user_location = request.user.locations.get(google_place_id=place_id, user=request.user)
            user_location.delete()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error'})


@login_required
def locations_search(request):
    if not request.GET.get('q'):
        return JsonResponse({})

    lat = request.GET.get('latitude')
    long = request.GET.get('longitude')
    places_json = find_places(request.GET.get('q'), lat=lat, long=long)
    return JsonResponse(places_json)


def _get_local_users(user, kind_to_connect):
    place_ids = [location.google_place_id for location in user.locations.all()]
    locations = UserLocation.objects.filter(google_place_id__in=place_ids)
    user_ids = set([location.user_id for location in locations])
    
    user_ids.discard(user.id)

    return User.objects.filter(id__in=user_ids,
        profile__kind=kind_to_connect, profile__is_publicly_visible=True)


@login_required
def local_users(request):
    user_profile = request.user.profile
    if not user_profile.kind:
        return redirect(reverse('profile_edit'))

    is_volunteer = request.user.profile.kind == UserProfile.VOLUNTEER
    if is_volunteer:
        kind_to_connect = UserProfile.SHELTERED
    else:
        kind_to_connect = UserProfile.VOLUNTEER

    location_count = request.user.locations.count()

    local_users = _get_local_users(request.user, kind_to_connect)

    return render(request, 'local-users.html', {
        'local_users': local_users,
        'location_count': location_count,
        'is_volunteer': is_volunteer
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        try:
            user = request.user
            auth_logout(request)
            user.delete()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error'})
            
    return JsonResponse({})
