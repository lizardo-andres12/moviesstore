from django.contrib import admin
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['name']

# class ReviewAdmin(admin.ModelAdmin):

# Movie model
admin.site.register(Movie, MovieAdmin)

# Review model
admin.site.register(Review)
