from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('resources/', views.resources, name='resources'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('settings/', views.account_settings, name='account_settings'),
    path('locations/', views.locations, name='locations'),
    path('local-users/', views.local_users, name='local_users'),
    path('locations/delete/', views.locations_delete, name='locations_delete'),
    path('locations/search/', views.locations_search, name='locations_search'),
    path('terms-of-use/', views.terms, name='terms'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('account/delete/', views.delete_account, name='delete_account'),
]