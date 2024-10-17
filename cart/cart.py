from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session found, create a new one
        if 'session_key' not in request.session:
            cart=self.session['session_key'] = {}

        # Make sure the cart is available on all pages of the site
        self.cart = cart

    def add(self, product):
        productId = str(product.id)

        # Check if the product is in the cart
        if productId in self.cart:
            # TODO: increase the quantity of the item in the cart
            pass
        else:
            # Add the product to the cart
            self.cart[productId] = {'price': str(product.price)}

        # Modify the session
        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def getProducts(self):
        # Get product ids currently in the cart
        productIds = self.cart.keys()

        # Use ids to look up products in the database model
        products = Product.objects.filter(id_in=productIds)

        # Return Products
        return products