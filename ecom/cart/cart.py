from store.models import Product, Profile



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

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
    
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #conert
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save cart to profile model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):

        product_id = str(product.id)
        product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
    
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #conert
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save cart to profile model
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # Get product IDs
        product_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for key, value in quantities.items():
            # Convert key string into int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + ( product.sale_price * value)
                    else:
                        total = total + ( product.price * value)
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

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # get cart
        ourcart = self.cart

        # update
        ourcart[product_id] = product_qty

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