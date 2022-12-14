import random
import os
import requests
import json
import base64
import time
from django.utils import timezone as tz
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from vibecheck.models import *

def index(request):
    if request.method != "POST":
        return render(request, "vibecheck/index.html")
    elif "access_token" in request.session and "expiration" in request.session and time.time() < request.session["expiration"]:
        request.session["vibe"] = request.POST.get("vibe")
        return redirect(reverse("show_playlist", args=[request.session["vibe"]]))
    else:
        request.session["vibe"] = request.POST.get("vibe")
        scope = "user-library-read playlist-modify-public"
        request.session["state"] = get_random_string(16)
        return redirect(f"https://accounts.spotify.com/authorize?client_id={os.getenv('SPOTIFY_CLIENT_ID')}&response_type=code&redirect_uri={os.getenv('SPOTIFY_REDIRECT_URI')}&state={request.session['state']}&scope={scope}&show_dialogue=true")

def callback(request):
    if request.GET["state"] != request.session["state"]:
        messages.error(request, 'Browser state does not match request state. Refresh browser.')
        return redirect("index")
    code = request.GET["code"]
    headers = {
        "Authorization": f"Basic {base64.b64encode((os.getenv('SPOTIFY_CLIENT_ID')+':'+os.getenv('SPOTIFY_CLIENT_SECRET')).encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv('SPOTIFY_REDIRECT_URI'),
    }
    response = requests.post(f"https://accounts.spotify.com/api/token", headers=headers, data=data)
    request.session["access_token"] = response.json()["access_token"] 
    request.session["expiration"] = time.time() + response.json()["expires_in"]
    return redirect(reverse("show_playlist", args=[request.session["vibe"]]))


def show_playlist(request, vibeid):    
    if time.time() >= request.session["expiration"]:
        return redirect("index")

    v = get_object_or_404(Vibe, id=vibeid)
    headers = {
        "Authorization": f"Bearer {request.session['access_token']}",
        "Content-Type": "application/json",
    }
    if request.method != "POST":
        vibeGenres = list(v.genres.all().values_list("name", flat=True))
        context = {"tracks": []}
        savedTrackIDs = []
        params = {"limit": 50}
        response = requests.get("https://api.spotify.com/v1/me/tracks", headers=headers, params=params)
        savedTracks = response.json()['items']

        if len(savedTracks) == 0: #no saved tracks, use all genres
            seedTracks = []
            seedGenres = vibeGenres

        else:
            for item in savedTracks:
                track = item['track'] 
                savedTrackIDs.append(track['id'])

        # recommendation engine is limited to 5 seeds only (3 tracks, 2 genres)
        # randomly pick 3 tracks from user saved tracks, randomly pick 2 genres from vibe table

            seedTracks = random.sample(savedTrackIDs, k=3)
            seedGenres = random.sample(vibeGenres, k=2)

        context["seedTracks"] = [f"{item['track']['artists'][0]['name']} – {item['track']['name']}" for item in savedTracks if item["track"]["id"] in seedTracks]
        context["seedGenres"] = seedGenres
        params = {
            "seed_tracks": seedTracks,
            "seed_genres": seedGenres,
        }
        response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params)
        recommendations = response.json()["tracks"]
        request.session["playlist"] = recommendations
        

        for track in recommendations:
            context["tracks"].append(f"{track['artists'][0]['name']} – {track['name']}")
    
        return render(request, "vibecheck/show_playlist.html", context)
        
    #save playlist on spotify
    else:
        response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        user_id = response.json()["id"]
        playlist_name = f"{v.name.capitalize()} Playlist {tz.now().month}/{tz.now().day}"
        data = json.dumps({
            "name": playlist_name,
            "description": "Created by VibeCheck",
            "public": True, 
        })
        response = requests.post(f"https://api.spotify.com/v1/users/{user_id}/playlists", data=data, headers=headers)
        playlist_id = response.json()['id']
        data = json.dumps({
            "uris": [request.session["playlist"][i]["uri"] for i in range(len(request.session["playlist"]))]
        })
        response = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", data=data, headers=headers)

        messages.success(request, f'Your playlist was saved successfully as "{playlist_name}"')

        #redirect back to home page
        return redirect("index")

