from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.account_settings, name='account_settings'),
    path('locations/', views.locations, name='locations'),
    path('locations/search/', views.locations_search, name='locations_search'),
    path('terms-of-use/', views.terms, name='terms'),
    path('privacy-policy/', views.privacy, name='privacy'),
]