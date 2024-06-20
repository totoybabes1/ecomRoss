from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from .models import Product, Category, Profile
from cart.cart import Cart
from django.db import transaction
from .decorators import login_required_custom
import json

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the product db model
        searched = Product.objects.filter(name__icontains=searched)
        messages.success(request, 'Product Found.... ') 
        if not searched:
            messages.success(request, 'Sorry Product Does not Exist.. ') 
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})

@login_required_custom
def update_info(request):
    # Ensure a ShippingAddress object exists for the user
    shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
    
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()
    
    form = UserInfoForm(request.POST or None, instance=profile)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    
    if form.is_valid() and shipping_form.is_valid():
        form.save()
        shipping_form.save()
        messages.success(request, 'Your information has been updated!')
        return redirect('index')
    
    return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})

@login_required_custom
def update_password(request):
    current_user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(current_user, request.POST)
        #is the form valid
        if form.is_valid():
            form.save()
            messages.success(request, "Your Password Has Been Updated.....")
            login(request, current_user)
            return redirect('update_user')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return redirect('update_password')
    else:
        form = ChangePasswordForm(current_user)
        return render(request, "update_password.html", {'form': form})

@login_required_custom
def update_user(request):
    current_user = User.objects.get(id=request.user.id)
    user_form = UpdateUserForm(request.POST or None, instance=current_user)

    if user_form.is_valid():
        user_form.save()
        login(request, current_user)
        messages.success(request, 'User has been Updated!!!.......')
        return redirect('index')
    return render(request,"update_user.html", {'user_form':user_form})

def category_summary(request):
    categories = Category.objects.all()  
    return render(request, 'category_summary.html', {"categories":categories})

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    # Replace Hypens with spaces
    foo = foo.replace('-', ' ')
    # grab the category on url
    try:
        #lookUp the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request,("Category Found!...."))    
        return redirect('index')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})

def index(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # lets do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their save cart from databese
            saved_cart = current_user.old_cart
            # convert database string to python dictionary
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #get cart
                cart = Cart(request)
                #loop tru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "You have been logged in.")    
            return redirect('index')
        else:
            messages.success(request, "There was an error.")    
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration complete.")
                return redirect('index')
            else:
                messages.error(request, "Authentication failed.")
        else:
            messages.error(request, "There is a problem with the form.")
    
    return render(request, 'register.html', {'form': form})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Order

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        if not product.in_stock:
            messages.error(request, "Sorry, this product is out of stock.")
            return redirect('product_detail', product_id=product_id)
        else:
            # Logic to add product to cart or handle purchase
            messages.success(request, f"{product.name} added to your cart.")
            return redirect('cart')

    return render(request, 'product.html', {'product': product})
