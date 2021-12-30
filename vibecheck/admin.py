from django.contrib import admin
from vibecheck.models import Genre, Vibe, UserVibe


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

admin.site.register(Genre, GenreAdmin)
admin.site.register(Vibe)
admin.site.register(UserVibe)