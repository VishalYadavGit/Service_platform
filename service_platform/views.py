from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import  SignupForm, LoginForm
from django.http import JsonResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
from .models import *
from .models import Service
from .ai import generate_caption

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@login_required(login_url='login')
def fixsolution(request):
    return render(request,'fixsolution.html')

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Service, Cart

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
    cart_item, created = Cart.objects.get_or_create(user=user, service=service,ispaid=False)

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
    cart_item = Cart.objects.get(user=user, service=service, ispaid=False)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')

@login_required(login_url='login')
def view_cart(request):
    # Replace this with your actual logic to get cart items for the current user
    user = request.user
    cart_items = Cart.objects.filter(user=user,ispaid=False)
    cart_total = sum(item.get_item_total() for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items,'cart_total': cart_total})

@login_required(login_url='login')
def book(request):
        form_type="User Registration"
        form_title="Book Now"
        return render(request,'book.html',{'form_type':form_type,'form_title':form_title})

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['confirm_password']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save()
                    messages.success(request, 'Registration successful. You can now log in.')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
        else:
            # Form is not valid, display the form with validation errors
            return render(request, 'register.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'register.html', {'form': form})

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

    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('/')

def detectit(request):
    if request.method=='POST':
        user_id = request.user.id
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        picture=request.FILES['picture']
        address=request.POST['address']
        pincode=request.POST['pincode']
        optionSelector=request.POST['optionSelector']
        print(user_id,name,email,phone,picture,address,pincode)
        instance=Booking.objects.create(user_id=user_id,name=name,email=email,phone=phone,picture=picture,address=address,pincode=pincode,job=optionSelector)
        instance.save()
        if optionSelector=="Plumber":
            products=Service.objects.filter(category='plumber',types='product')
        if optionSelector=="Electrician":
            products=Service.objects.filter(category='electrician',types='product')
        return render(request,'confirmation.html',{'products':products})
    user = request.user
    last_object=Booking.objects.filter(user=user).order_by('-created_at').first()
    if last_object.job=="Plumber":
        products=Service.objects.filter(category='plumber',types='product')
    if last_object.job=="Electrician":
            products=Service.objects.filter(category='electrician',types='product')
    return render(request,'confirmation.html',{'products':products})
    
def ai(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        caption, time = generate_caption(uploaded_file)
        electrician = [
    'electrician', 'electrical', 'wiring', 'circuit', 'outlet', 'switch', 'lighting', 'resistor', 
    'conduit', 'breaker', 'wire', 'volt', 'amp', 'socket', 'junction box', 'grounding', 'generator', 
    'transformer', 'cable', 'fuse', 'meter', 'insulation', 'power', 'voltage', 'current', 'ohm', 
    'electric panel', 'receptacle', 'electrical code', 'circuit breaker', 'electrical contractor', 
    'electrical work', 'watt', 'kilowatt', 'electrical system', 'short circuit', 'ohmmeter', 'multimeter', 
    'electrical repair', 'electrical service'
]
        plumber = [
    'plumber', 'plumbing', 'pipe', 'leak', 'faucet', 'valve', 'wrench', 'sewer', 'drain', 
    'clog', 'pipefitter', 'pipefitting', 'water', 'fixture', 'soldering', 'sealant', 
    'plunger', 'toilet', 'flush', 'copper', 'pex', 'galvanized', 'pipe wrench', 'pipe cutter', 
    'snake', 'auger', 'plumbing code', 'water heater', 'plumbing fixture', 'gasket', 'joint', 
    'plumbing system', 'vent', 'trap', 'pressure', 'backflow', 'plumbing repair', 'plumbing service','faucet'
]
        def is_related_to_plumber(input_string):
         for word in plumber:
          if word in input_string:
           return True
         return False
        def is_related_to_electrician(input_string):
         for word in electrician:
          if word in input_string:
           return True
         return False
        conclusion = ""
        if is_related_to_electrician(caption):
            conclusion = "Electrician"
        else:
            is_related_to_plumber(caption)
            conclusion = "Plumber"
            
        return JsonResponse({'status': 'success', 'message': caption,'conclusion':conclusion,})
    else:
        return JsonResponse({'status': 'error', 'message': 'No file found in the request'})
    
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user,ispaid=False)
    cart_total = sum(item.get_item_total() for item in cart_items)
    if request.method=='POST':
       if cart_total>0:
        user_id = request.user.id
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        pincode=request.POST['pincode']
        instance=Booking.objects.create(user_id=user_id,name=name,email=email,phone=phone,address=address,pincode=pincode)
        instance.save()
        products=Service.objects.all()
        Cart.objects.filter(user=request.user).update(ispaid=True)
        return render(request,'confirmation.html',{'products':products})
       else:
        messages.error(request, 'Cart is empty')
        return redirect('view_cart')
    form_type="Fill Your Address Details"
    form_title="Address"
    return render(request,'book.html',{'form_type':form_type,'form_title':form_title,'cart_total':cart_total})