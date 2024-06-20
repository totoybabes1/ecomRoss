from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm , PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    context = {
        'orders': orders
    }
    return render(request, 'payment/order_history.html', context)


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, "payment/not_shipped_dash.html", {"orders":orders})
    else:
        messages.success(request,"Access Denied!")
        return redirect ('index')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request,"Access Denied!")
        return redirect ('index')

def process_order(request):
    if request.POST:
        # Get cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get the billing info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get the shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        # Create Shipping_Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals

        # Create order
        if request.user.is_authenticated:
            user = request.user
            # Create order
            create_order = Order(user=user, full_name=full_name, email=email, Shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get the order id
            order_id = create_order.pk
            
            # Get product details
            for product in cart_products():
                # Get product id
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user_id=user.id, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart 
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete key
                    del request.session[key]

            messages.success(request, "Order Placed")
            return redirect('index')
        else:
            # Not logged in
            create_order = Order(full_name=full_name, email=email, Shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Delete our cart 
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete key
                    del request.session[key]
            
            messages.success(request, "Order Placed")
            return redirect('index')
        
    else:
        messages.success(request, "Access Denied")
        return redirect('index')



def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #create a session with  shipping_info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals,  "shipping_info":request.POST, "billing_form":billing_form})
  
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals,  "shipping_info":request.POST,  "billing_form":billing_form})
  

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals,  "shipping_form":shipping_form})
    else:
        messages.success(request, "Access Deniad")
        return redirect('index')





def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form":shipping_form })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals,  "shipping_form":shipping_form})

  



# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html",{})