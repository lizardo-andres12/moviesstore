from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['name']

admin.site.register(Movie, MovieAdmin)
