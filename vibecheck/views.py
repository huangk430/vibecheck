import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from project_vibecheck.settings import LOGIN_REDIRECT_URL
import spotipy
from spotipy.oauth2 import SpotifyOAuth




# Create your views here.
def index(request):
    context = {"message": "good morning"}
    studs = ["bob", "jimmy", "david", "kelly", "joe"]
    context["students"] = [{"name": s, "grade": random.randint(0,100)} for s in studs]
    return render(request, "vibecheck/index.html", context)

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


@login_required
def show_playlist(request, vibeid):
    scope = "user-library-read"
    context = {"tracks": []}
    seedTracks = []
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    savedTracks = sp.current_user_saved_tracks()
    #print(savedTracks)
    for idx, item in enumerate(savedTracks['items']):
        track = item['track'] 
        seedTracks.append(track['id'])
    
    results = sp.recommendations(seed_tracks=seedTracks[:5])
    print(results)

    for idx, track in enumerate(results['tracks']):
        context["tracks"].append(f"{idx} {track['artists'][0]['name']} –  {track['name']}<br>")
   
    return render(request, "vibecheck/show_playlist.html", context)










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
