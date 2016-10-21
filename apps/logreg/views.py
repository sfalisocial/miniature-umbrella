from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'logreg/index.html')

def success(request):
    if 'logged_user' not in request.session:
        messages.error(request, "You must login to view this page!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['logged_user'])
    }
    return render(request, 'logreg/success.html', context)

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid login")
        else:
            request.session['logged_user'] = user.id
            messages.success(request, "Welcome {}!".format(user.first_name))
            return redirect('success')
    return redirect('logreg_index')

def register(request):
    if request.method == "POST":
        form_errors = User.objects.validate_user_info(request.POST)
        #if there are errors, throw them into flash messages
        if len(form_errors)> 0:
            for error in form_errors:
                messages.error(request, error)
        else:
            user = User.objects.register(request.POST)
            messages.success(request, "You have successfully registered!")
    return redirect('logreg_index')

def logout(request):
    if 'logged_user' in request.session:
        request.session.pop('logged_user')
        messages.success(request, "You have successfully logged out!")
    return redirect('logreg_index')
