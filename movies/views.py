from django.shortcuts import render
from .models import Movie

def index(request):
    """Displays catalog of all movies, or displays search results for `search=*`."""

    # Get value of request param `search` or falsey-value if key is not present in URL query.
    search_term = request.GET.get('search')

    # Find movies desired based on query.
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    # Render a response to the client.
    template_data = {
        'title': 'Movies',
        'movies': movies,
    }
    return render(request, 'movies/index.html', {
        'template_data': template_data
    })

def show(request, id):
    movie = Movie.objects.get(id=id)
    template_data = {
        'title': movie.name,
        'movie': movie
    }
    return render(request, 'movies/show.html', {
        'template_data': template_data
    })
