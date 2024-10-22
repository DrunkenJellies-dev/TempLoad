from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get Request
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session found, create a new one
        if 'session_key' not in request.session:
            cart=self.session['session_key'] = {}

        # Make sure the cart is available on all pages of the site
        self.cart = cart

    def dbAdd(self, product, quantity):
        productId = str(product)
        productQty = str(quantity)

        # Check if the product is in the cart
        if productId in self.cart:
            # TODO: increase the quantity of the item in the cart
            pass
        else:
            # Add the product to the cart
            self.cart[productId] = int(productQty)

        # Modify the session
        self.session.modified = True

        # Deal with logged in users
        if self.request.user.is_authentication:
            # Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)

            # Convert to string
            stringCart = str(self.cart)
            stringCart = stringCart.replace("\'", "\"")

            # Save stringCart to the profile Model
            currentUser.update(oldCart=str(stringCart))

    def add(self, product, quantity):
        productId = str(product.id)
        productQty = str(quantity)

        # Check if the product is in the cart
        if productId in self.cart:
            # TODO: increase the quantity of the item in the cart
            pass
        else:
            # Add the product to the cart
            self.cart[productId] = int(productQty)

        # Modify the session
        self.session.modified = True

        # Deal with logged in users
        if self.request.user.is_authenticated:
            # Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)

            # Convert to string
            stringCart = str(self.cart)
            stringCart = stringCart.replace("\'", "\"")

            # Save stringCart to the profile Model
            currentUser.update(oldCart=str(stringCart))
            

    def cartTotal(self):
        # Get product ids currently in the cart
        productIds = self.cart.keys()

        # Find keys in products database model
        products = Product.objects.filter(id__in=productIds)

        # Get Quantities
        quantities = self.cart

        # Initializing total starting at 0
        total=0
        # Loop through items in the cart and get the key and value
        for key, value in quantities.items():
            # Convert key string to int
            key = int(key)
            # Loop through all products
            for product in products:
                # Check if the product in cart matches a product in database
                if product.id == key:
                    # Check if the product is on sale
                    if product.isSale:
                        # Add the price to the total times the price for items on sale
                        total = total + (product.salePrice * value)
                    else:
                        # Add the price to the total times the price
                        total = total + (product.price * value)

        return total



    def __len__(self):
        return len(self.cart)
    
    def getProducts(self):
        # Get product ids currently in the cart
        productIds = self.cart.keys()

        # Use ids to look up products in the database model
        products = Product.objects.filter(id__in=productIds)

        # Return Products
        return products
    
    def getQuantities(self):
        # Get quantities
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        # Get inputs and store as variables {'4':3, '2':5} -> The data stored in the cart
        productId = str(product)
        productQty = int(quantity)

        # Get cart
        cart = self.cart

        # Update cart
        cart[productId] = productQty

        # Setting session modified to True
        self.session.modified = True

        # Deal with logged in users
        if self.request.user.is_authentication:
            # Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)

            # Convert to string
            stringCart = str(self.cart)
            stringCart = stringCart.replace("\'", "\"")

            # Save stringCart to the profile Model
            currentUser.update(oldCart=str(stringCart))

        # Return the cart
        return self.cart
    
    def delete(self, product):
        # Get inputs and store as variables {'4':3, '2':5} -> The data stored in the cart
        productId = str(product)

        # Get cart
        cart = self.cart

        #Delete the product from cart
        if productId in self.cart:
            del self.cart[productId]

        # Setting session modified to True
        self.session.modified = True

        # Deal with logged in users
        if self.request.user.is_authentication:
            # Get the current user profile
            currentUser = Profile.objects.filter(user__id=self.request.user.id)

            # Convert to string
            stringCart = str(self.cart)
            stringCart = stringCart.replace("\'", "\"")

            # Save stringCart to the profile Model
            currentUser.update(oldCart=str(stringCart))

        # Return the cart
        return self.cart