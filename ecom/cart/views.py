from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':  # Corrected the spacing around 'post'
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)
       
        #save session
        cart.add(product=product, quantity=product_qty)

        #get cart quantity
        cart_quantity = cart.__len__()


        #return response
        response = JsonResponse({'Product Name': product.name})
        messages.success(request,("Product Added to Cart......"))
        #response = JsonResponse({'qty': cart_quantity})
        return response
    
    else:
        response = JsonResponse({'error': 'Invalid request'})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request,("Item Deleted......"))
        return response
    else:
        return JsonResponse({'error': 'Invalid request'})


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request,("Your Product Updated......"))
        return response
        #return redirect('cart_summary')
