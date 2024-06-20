from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
import datetime

# Define the fixed shipping fee
FIXED_SHIPPING_FEE = 300  # Or whatever your fixed shipping fee amount is

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    for order in orders:
        order.date_ordered_formatted = order.date_ordered.strftime('%Y-%m-%d %I:%M %p')
    context = {'orders': orders}
    return render(request, 'payment/order_history.html', context)

@login_required
def orders(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect('index')

    order = Order.objects.get(id=pk)
    items = OrderItem.objects.filter(order=pk)
    order.date_ordered_formatted = order.date_ordered.strftime('%Y-%m-%d %I:%M %p')

    if request.method == 'POST':
        status = request.POST['shipping_status']
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %I:%M %p')  # Format time as 12-hour clock

        if status == "true":
            order.shipped = True
            order.date_shipped = now
            order.save()

            confirmation_link = request.build_absolute_uri(reverse('confirm_shipment', args=[order.id]))
            subject = 'Order Shipped'
            html_message = render_to_string('emails/order_shipped_email.html', {
                'full_name': order.full_name,
                'order_id': order.id,
                'shipping_address': order.shipping_address,
                'confirmation_link': confirmation_link,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = [order.email]

            email_message = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
            email_message.attach_alternative(html_message, "text/html")
            email_message.send(fail_silently=False)
        else:
            order.shipped = False
            order.save()

        messages.success(request, "Shipping Status Updated")
        return redirect('index')

    return render(request, 'payment/orders.html', {"order": order, "items": items})

@login_required
def confirm_shipment(request, pk):
    order = Order.objects.get(pk=pk)
    order.confirmed_shipment = True
    order.save()
    return redirect('index')

@login_required
def not_shipped_dash(request):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect('index')

    orders = Order.objects.filter(shipped=False)
    for order in orders:
        order.date_ordered_formatted = order.date_ordered.strftime('%Y-%m-%d %I:%M %p')

    if request.method == 'POST':
        status = request.POST['shipping_status']
        order_id = request.POST['num']
        order = Order.objects.get(id=order_id)
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %I:%M %p')  # Format time as 12-hour clock

        if status == "true":
            order.shipped = True
            order.date_shipped = now
            order.save()
            messages.success(request, "Shipping Status Updated")
        return redirect('index')

    return render(request, "payment/not_shipped_dash.html", {"orders": orders})

@login_required
def shipped_dash(request):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect('index')

    orders = Order.objects.filter(shipped=True)
    for order in orders:
        order.date_ordered_formatted = order.date_ordered.strftime('%Y-%m-%d %I:%M %p')

    if request.method == 'POST':
        status = request.POST['shipping_status']
        order_id = request.POST['num']
        order = Order.objects.get(id=order_id)

        if status == "false":
            order.shipped = False
            order.save()
            messages.success(request, "Shipping Status Updated")
        return redirect('index')

    return render(request, "payment/shipped_dash.html", {"orders": orders})

@login_required
def process_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        shipping_fee = FIXED_SHIPPING_FEE
        transaction_id = request.POST.get('gcash_transaction_id')
        sender_name = request.POST.get('gcash_sender_name')
        sender_number = request.POST.get('cod_contact_number')
        my_shipping = request.session.get('my_shipping')

        # Check if my_shipping exists in session
        if my_shipping is None:
            messages.error(request, "Shipping information is missing.")
            return redirect('index')

        # Access shipping details from my_shipping dictionary
        full_name = my_shipping.get('shipping_full_name')
        email = my_shipping.get('shipping_email')
        shipping_address = f"{my_shipping.get('shipping_address1')}\n{my_shipping.get('shipping_address2')}\n{my_shipping.get('shipping_city')}\n{my_shipping.get('shipping_state')}\n{my_shipping.get('shipping_zipcode')}\n{my_shipping.get('shipping_country')}"
        amount_paid = totals + shipping_fee

        user = request.user if request.user.is_authenticated else None
        create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, transaction_id=transaction_id, sender_name=sender_name, sender_number=sender_number)
        create_order.save()

        # Create OrderItem objects for each product in the cart
        for product in cart_products:
            price = product.sale_price if product.is_sale else product.price
            quantity = quantities.get(product.id, 0)  # Use .get() method with a default value
            OrderItem.objects.create(order=create_order, product=product, user=user, quantity=quantity, price=price)

        # Clear the cart
        cart.clear()

        # Clear session data
        request.session.pop('my_shipping', None)

        # Update user's profile
        if user:
            Profile.objects.filter(user__id=user.id).update(old_cart="")

        messages.success(request, "Order Placed!")

        # Send order confirmation email
        subject = 'Order Confirmation'
        html_message = render_to_string('emails/order_confirmation_email.html', {
            'full_name': full_name,
            'order_id': create_order.id,
            'amount_paid': amount_paid,
            'shipping_address': shipping_address,
            'date_ordered': create_order.date_ordered.strftime('%Y-%m-%d %I:%M %p')
        })
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        email_message = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
        email_message.attach_alternative(html_message, "text/html")
        email_message.send(fail_silently=False)

        return redirect('index')

    else:
        messages.error(request, "Access Denied")
        return redirect('index')





@login_required
def billing_info(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        subtotal = cart.cart_total()
        shipping_fee = FIXED_SHIPPING_FEE
        total_amount = subtotal + shipping_fee  # Calculate the total amount

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        billing_form = PaymentForm()
        return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "subtotal": subtotal, "shipping_fee": shipping_fee, "total_amount": total_amount, "shipping_info": my_shipping, "billing_form": billing_form})

    else:
        messages.error(request, "Access Denied")
        return redirect('index')

@login_required
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    subtotal = cart.cart_total()
    shipping_fee = FIXED_SHIPPING_FEE
    total_amount = subtotal + shipping_fee  # Calculate the total amount

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)
    
    return render(request, "payment/checkout.html", {
        "cart_products": cart_products, 
        "quantities": quantities, 
        "subtotal": subtotal, 
        "shipping_fee": shipping_fee, 
        "total_amount": total_amount, 
        "shipping_form": shipping_form
    })

def payment_success(request):
    return render(request, "payment/payment_success.html", {})
