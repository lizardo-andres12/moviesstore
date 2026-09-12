from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Movie, Report, Review

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
    """Displays the page for a single movie, including description, price, image, and reviews."""
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    # Fetch all reported reviews for this specific movie.
    reported_review_ids = set([report.review.id for report in Report.objects.filter(movie=movie)])
    # Remove all reviews that have been reported.
    reviews = [review for review in reviews if review.id not in reported_review_ids]

    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews,
    }
    return render(request, 'movies/show.html', {
        'template_data': template_data
    })

@login_required
def create_review(request, id):
    """Handle post request to create comment (`models.Review`) for Movie with ID `id`"""
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id)
    else:
        return redirect('movies.show', id)

@login_required
def edit_review(request, id, review_id):
    """Takes a movie ID, a review ID, and an updated comment to change review[id].comment to."""
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {
            'title': 'Edit Review',
            'review': review,
        }
        return render(request, 'movies/edit_review.html', {
            'template_data': template_data
        })
    elif request.method == 'POST' and request.POST['comment'] != '':
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    """Takes a movie ID and review ID to delete a review for movie."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)

    report = Report()
    report.movie = review.movie
    report.review = review
    report.reportee = review.user
    report.reporter = request.user
    report.save()
    return redirect('movies.show', id=id)
