from project_vibecheck.settings import LOGIN_REDIRECT_URL
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import random

# Create your views here.
def index(request):
    context = {"message": "good morning"}
    studs = ["bob", "jimmy", "david", "kelly", "joe"]
    context["students"] = [{"name": s, "grade": random.randint(0,100)} for s in studs]
    return render(request, "vibecheck/index.html", context)

@login_required
def home(request):
    context = {}
    return render(request, "vibecheck/home.html", context)