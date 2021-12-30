from django.shortcuts import render
import random
# Create your views here.
def index(request):
    context = {"message": "good morning"}
    studs = ["bob", "jimmy", "david", "kelly", "joe"]
    context["students"] = [{"name": s, "grade": random.randint(0,100)} for s in studs]
    return render(request, "vibecheck/index.html", context)

def home(request):
    context = {}
    return render(request, "vibecheck/home.html", context)