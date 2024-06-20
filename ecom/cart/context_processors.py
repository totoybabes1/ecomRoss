from .cart import Cart
    #CREATE CONTEXT PROCESSOR

def cart(request):
    #request default data from our cart
    return {'cart': Cart(request)}