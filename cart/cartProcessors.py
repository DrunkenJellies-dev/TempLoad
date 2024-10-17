from .cart import Cart

# Create context processor so the cart works on all pages of the site
def cart(request):
    # Return the default data from our Cart
    return {'cart':Cart(request)}