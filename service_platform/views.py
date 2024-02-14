from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.http import JsonResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
from .models import *
# Create your views here.
from .forms import  SignupForm, LoginForm
from .ai import generate_caption
# views.py

from .models import Service
from .ai import generate_caption

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')
def fixsolution(request):
    return render(request,'fixsolution.html')


# views.py
from django.db.models import Q
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Service, Cart

# views.py
from django.db.models import Q

def product(request):
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    action = request.GET.get('action')

    products = Service.objects.filter(types='product')
    print(products)
    if category_filter:
        products = products.filter(category=category_filter)
    
    if action == 'search' and search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    # Check if the reset button is clicked, and reset both category_filter and search_query
    if action == 'reset':
        category_filter = ''
        search_query = ''

    for product in products:
        # Split descriptions into a list
        product.description_list = product.description.split("\n")



    return render(request, 'product.html', {'products': products, 'category_filter': category_filter, 'search_query': search_query})
def service(request):
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    action = request.GET.get('action')

    services = Service.objects.filter(types='service')
    

    if category_filter:
        services = services.filter(category=category_filter)
    
    if action == 'search' and search_query:
        services = services.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    # Check if the reset button is clicked, and reset both category_filter and search_query
    if action == 'reset':
        category_filter = ''
        search_query = ''

    for service in services:
        # Split descriptions into a list
        service.description_list = service.description.split("\n")

    return render(request, 'service.html', {'services': services, 'category_filter': category_filter, 'search_query': search_query})




def add_to_cart(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    user = request.user

    # Check if the item is already in the cart for this user
    cart_item, created = Cart.objects.get_or_create(user=user, service=service)

    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    referring_url = request.META.get('HTTP_REFERER', '/fallback-url/')

    return redirect(referring_url)

def remove_item(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    user = request.user

    # Check if the item is already in the cart for this user
    cart_item = Cart.objects.get(user=user, service=service)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')

def view_cart(request):
    # Replace this with your actual logic to get cart items for the current user
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    cart_total = sum(item.get_item_total() for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items,'cart_total': cart_total})

@login_required(login_url='login')
def book(request):
        return render(request,'book.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name'] #first_name is the name of the input field in register.html
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1'] #password1 is the name of the input field in register.html
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username = username).exists(): #check if the username already exists
                messages.info(request,'Username taken')
                return redirect('register') #redirect to the register page if the username already exists
            elif User.objects.filter(email = email).exists(): #check if the email already exists
                messages.info(request,'Email taken')
                return redirect('register') #redirect to the register page if the email already exists
            else:
                user = User.objects.create_user(username = username, password = password1, email = email, first_name = first_name, last_name = last_name) #create a user
                user.save() #save the user
                print('User created')
                return redirect('login') #redirect to the login page after the user is created
        else:
            messages.info(request,'Password not matching')
            return redirect('register') #redirect to the register page if the password doesn't match
        return redirect('/')
    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form,'message':messages})


def logout(request):
    auth.logout(request)
    return redirect('/')

from .forms import SignupForm

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username, email=email, password=password)
                    auth.login(request, user)
                    return redirect('/')
                else:
                    form.add_error('username', 'Username is already taken.')
            else:
                form.add_error('confirm_password', 'Passwords do not match.')
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})

def detectit(request):
    if request.method=='POST':
        user_id = request.user.id
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        picture=request.FILES['picture']
        address=request.POST['address']
        pincode=request.POST['pincode']
        print(user_id,name,email,phone,picture,address,pincode)
        instance=Booking.objects.create(user_id=user_id,name=name,email=email,phone=phone,picture=picture,address=address,pincode=pincode)
        instance.save()
       

def ai(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        caption, time = generate_caption(uploaded_file)
        
        return JsonResponse({'status': 'success', 'message': caption})
    else:
        return JsonResponse({'status': 'error', 'message': 'No file found in the request'})
    
    