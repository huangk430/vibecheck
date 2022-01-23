from django import forms
from vibecheck.models import * 

class VibeForm(forms.Form):
    vibe = forms.ModelChoiceField(queryset=Vibe.objects.all(), required=True)