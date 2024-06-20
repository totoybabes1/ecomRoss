from store.models import Product, Profile
from decimal import Decimal  # Import Decimal module


class Cart():
    def __init__(self, request):
        self.session = request.session
        # get request
        self.request = request
        # get current session 
        cart = self.session.get('session_key')

        # if the user is new , no session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure available on all pages
        self.cart = cart

    def clear(self):
        self.cart = {}  # Set cart to an empty dictionary
        self.session.modified = True

    def db_add(self, product, quantity):
        product_id = str(product)
        
        if isinstance(quantity, dict):
            product_qty = quantity.get('quantity', 0)
            foot_size = quantity.get('foot_size')
        else:
            product_qty = quantity
            foot_size = None

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'quantity': int(product_qty), 'foot_size': foot_size}

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", "\"")
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity, foot_size=None):  # Modify add method signature
        product_id = str(product.id)
        product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = {'quantity': int(product_qty), 'foot_size': foot_size}  # Store foot size

        self.session.modified = True


    def cart_total(self):
        total = Decimal(0)  # Initialize total as Decimal

        for product_id, quantity in self.cart.items():
            if isinstance(quantity, dict):  # Check if quantity is a dictionary
                quantity = quantity.get('quantity', 0)  # Extract the 'quantity' value
            quantity = Decimal(quantity)  # Convert quantity to Decimal
            product = Product.objects.get(id=product_id)
            if product.is_sale:
                total += product.sale_price * quantity
            else:
                total += product.price * quantity

        return total





    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()
        # use ids to lookup product in database model
        products = Product.objects.filter(id__in=product_ids)
        # return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity, foot_size=None):  # Modify update method signature
        product_id = str(product)
        product_qty = int(quantity)
        # get cart
        ourcart = self.cart

        # update
        ourcart[product_id] = {'quantity': product_qty, 'foot_size': foot_size}  # Store foot size

        self.session.modified = True


     

        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #conert
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save cart to profile model
            current_user.update(old_cart=str(carty))

            
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[str(product)]
        self.session.modified = True
       
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #conert
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save cart to profile model
            current_user.update(old_cart=str(carty))