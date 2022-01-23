#business logic
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from project_vibecheck.settings import LOGIN_REDIRECT_URL
from vibecheck.forms import *
# Create your views here.
class VibeCheckLoginView(LoginView):
    template_name = "vibecheck/index.html"


@login_required
def index(request):
    context = {}
    scope = "user-library-read"

    if request.method == "GET":
        form = VibeForm()
    elif request.method == "POST":
        form = VibeForm(request.POST)
        if form.is_valid():
            return redirect(f"show_playlist/{form.cleaned_data['vibe'].id}/")
    context["form"] = form
    return render(request, "vibecheck/home.html", context)


@login_required
def show_playlist(request, vibeid):
    scope = "user-library-read"
    context = {"vibe": vibeid, "tracks": []}
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_saved_tracks()

    for idx, item in enumerate(results['items']):
        track = item['track']
        context["tracks"].append(f"{idx} {track['artists'][0]['name']} –  {track['name']}") 
    return render(request, "vibecheck/show_playlist.html", context)
