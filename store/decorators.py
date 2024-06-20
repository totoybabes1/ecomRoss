from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def login_required_custom(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('index')  # Replace 'homepage' with the name of your homepage URL pattern
    return wrap
