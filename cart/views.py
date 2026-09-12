from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from movies.models import Movie

from .models import Item, Order
from .utils import calculate_cart_total

def index(request):
    cart_total = 0
    movies = []

    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if movie_ids:
        movies = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies)

    template_data = {
        'title': 'Cart',
        'movies_in_cart': movies,
        'cart_total': cart_total,
    }
    return render(request, 'cart/index.html', {
        'template_data': template_data
    })

def clear(request):
    """Removes all items from cart for request.session."""
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    """Creates Order and Item(s) with all movies in request.session['cart']."""
    cart = request.session.get('cart', {})
    movie_ids = cart.keys()
    if not movie_ids:
        return redirect('cart.index')
    movies = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies)

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()

    for movie in movies:
        item = Item()
        item.price = movie.price
        item.quantity = cart[str(movie.id)]
        item.movie = movie
        item.order = order
        item.save()

    request.session['cart'] = {}
    template_data = {
        'title': 'Purchase Confirmation',
        'order_id': order.id,
    }
    return render(request, 'cart/purchase.html', {
        'template_data': template_data
    })

def add(request, id):
    """Adds movie corresponding to ID to session['cart']."""
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']  # Might need to ensure this exists.
    request.session['cart'] = cart
    return redirect('cart.index')
