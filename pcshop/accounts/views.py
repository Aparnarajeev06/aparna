from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Address
from orders.models import Order
from support.models import Ticket, RMARequest

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Update additional profile info if desired
            phone = request.POST.get('phone', '')
            bio = request.POST.get('bio', '')
            if phone or bio:
                profile = user.profile
                profile.phone = phone
                profile.bio = bio
                profile.save()
            
            login(request, user)
            messages.success(request, f"Welcome to NOVA TECH, {user.username}! Your gaming account is active.")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Registration details invalid. Please review errors.")
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'accounts:dashboard')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def admin_login_view(request):
    """Custom admin login page for staff users"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, f"Welcome back, Admin {username}! System access granted.")
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "Access denied. Admin credentials required.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/admin_login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out. Game on!")
    return redirect('home')

@login_required
def dashboard_view(request):
    user = request.user
    # Get profile (auto-created via signals)
    profile = user.profile
    # Get orders
    orders = Order.objects.filter(user=user).order_by('-created_at')
    # Get addresses
    addresses = Address.objects.filter(user=user).order_by('-is_default', '-id')
    # Get tickets
    tickets = Ticket.objects.filter(user=user).order_by('-created_at')
    # Get RMAs
    rmas = RMARequest.objects.filter(user=user).order_by('-created_at')

    context = {
        'profile': profile,
        'orders': orders,
        'addresses': addresses,
        'tickets': tickets,
        'rmas': rmas
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_edit_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, "Profile telemetry updated successfully.")
        return redirect('accounts:dashboard')
    return render(request, 'accounts/profile_edit.html', {'profile': profile})

@login_required
def add_address_view(request):
    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country', 'USA')
        is_default = request.POST.get('is_default') == 'true'

        if street and city and postal_code:
            Address.objects.create(
                user=request.user,
                street=street,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                is_default=is_default
            )
            messages.success(request, "Address successfully registered.")
        else:
            messages.error(request, "Missing address parameters.")
    return redirect('accounts:dashboard')

@login_required
def delete_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Address deleted from your registry.")
    return redirect('accounts:dashboard')

@login_required
def make_default_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, "Primary address selection updated.")
    return redirect('accounts:dashboard')
