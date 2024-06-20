from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from .decorators import login_required_custom
from .cart import Cart
from store.models import Product

@login_required_custom
def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

@login_required_custom
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        foot_size = request.POST.get('foot_size')  # Get foot size

        product = get_object_or_404(Product, id=product_id)
       
        # Save session
        cart.add(product=product, quantity=product_qty, foot_size=foot_size)  # Pass foot size

        # Get cart quantity
        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({'Product Name': product.name})
        messages.success(request, "Product Added to Cart...")
        return response
    
    else:
        response = JsonResponse({'error': 'Invalid request'})
        return response


@login_required_custom
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, "Item Deleted......")
        return response
    else:
        return JsonResponse({'error': 'Invalid request'})

@login_required_custom
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        foot_size = request.POST.get('foot_size')  # Get foot size

        cart.update(product=product_id, quantity=product_qty, foot_size=foot_size)  # Pass foot size

        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Your Product Updated...")
        return response
    else:
        return JsonResponse({'error': 'Invalid request'})

