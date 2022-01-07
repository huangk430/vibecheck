import random
from django.shortcuts import render
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
    context = {"tracks": ""}
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        context["tracks"] += f"{idx} {track['artists'][0]['name']} –  {track['name']}<br>"
    
    return render(request, "vibecheck/home.html", context)
