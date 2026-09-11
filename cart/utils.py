def calculate_cart_total(cart, movies_in_cart):
    """Returns the sum of all movies in cart."""
    return sum([int(cart[str(movie.id)]) * movie.price for movie in movies_in_cart])
