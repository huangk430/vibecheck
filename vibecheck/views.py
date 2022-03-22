import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from project_vibecheck.settings import LOGIN_REDIRECT_URL
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from vibecheck.models import *




# Create your views here.
def index(request):
    if request.method != "POST":
        context = {}
        return render(request, "vibecheck/index.html", context)
    else:
        print(request.POST)
        return redirect(reverse("show_playlist", args=[request.POST.get("vibe")]))


@login_required
def show_playlist(request, vibeid):
    # v = Vibe.objects.get(id=vibeid)
    v = get_object_or_404(Vibe, id=vibeid)
    genreSeeds = v.genres.all().values_list("name", flat=True)
    scope = "user-library-read"
    context = {"tracks": []}
    seedTracks = []
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    savedTracks = sp.current_user_saved_tracks()
    #print(savedTracks)
    for idx, item in enumerate(savedTracks['items']):
        track = item['track'] 
        seedTracks.append(track['id'])

    # TODO recommendation engine is limited to 5 seeds only (3 tracks, 2 genres)
    # TODO randomly pick 3 tracks from user saved tracks, randomly pick 2 genres from vibe table


    results = sp.recommendations(seed_genres=genreSeeds)
    # print(results)

    for idx, track in enumerate(results['tracks']):
        context["tracks"].append(f"{idx} {track['artists'][0]['name']} –  {track['name']}<br>")
   
    return render(request, "vibecheck/show_playlist.html", context)

@login_required
def home(request):
    context = {"tracks": []}
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        context["tracks"].append(f"{idx} {track['artists'][0]['name']} –  {track['name']}<br>")
    
    if request.method != "POST":
        return render(request, "vibecheck/home.html", context)
    else:
        return redirect(reverse("show_playlist", args=[1]))










# #business logic
# import os
# import random
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from allauth.account.views import LoginView
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from project_vibecheck.settings import LOGIN_REDIRECT_URL
# from vibecheck.forms import *
# # Create your views here.
# class VibeCheckLoginView(LoginView):
#     template_name = "vibecheck/index.html"


# @login_required
# def index(request):
#     context = {}

#     if request.method == "GET":
#         form = VibeForm()
#     elif request.method == "POST":
#         form = VibeForm(request.POST)
#         if form.is_valid():
#             return redirect(f"show_playlist/{form.cleaned_data['vibe'].id}/")
#     context["form"] = form
#     return render(request, "vibecheck/home.html", context)


# @login_required
# def show_playlist(request, vibeid):
#     scope = "user-library-read"
#     client_id = os.getenv("SPOTIPY_CLIENT_ID")
#     client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
#     redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
#     context = {"vibe": vibeid, "tracks": []}
#     breakpoint()
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#     results = sp.current_user_saved_tracks()

#     for idx, item in enumerate(results['items']):
#         track = item['track']
#         context["tracks"].append(f"{idx} {track['artists'][0]['name']} –  {track['name']}") 
#     return render(request, "vibecheck/show_playlist.html", context)
