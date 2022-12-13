from django.contrib import admin
from vibecheck.models import *


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

admin.site.register(Genre, GenreAdmin)
admin.site.register(Vibe)
