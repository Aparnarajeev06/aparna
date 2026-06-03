from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.views import get_or_create_cart
from cart.models import Cart, CartItem
from accounts.models import Address
from .models import Order, OrderItem
from products.models import Product

@login_required
def checkout_view(request):
    cart = get_or_create_cart(request)
    
    if cart.items.count() == 0:
        messages.error(request, "Your shopping cart is empty! Add gaming gear to check out.")
        return redirect('cart:detail')
        
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Retrieve shipping address details
        address_id = request.POST.get('address_id')
        if address_id:
            addr_obj = get_object_or_404(Address, id=address_id, user=request.user)
            shipping_address = f"{addr_obj.street}, {addr_obj.city}, {addr_obj.state} {addr_obj.postal_code}, {addr_obj.country}"
        else:
            street = request.POST.get('street')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            country = request.POST.get('country', 'USA')
            
            if not street or not city or not postal_code:
                messages.error(request, "Please select or enter a valid shipping address.")
                return render(request, 'orders/checkout.html', {'cart': cart, 'addresses': addresses})
                
            shipping_address = f"{street}, {city}, {state} {postal_code}, {country}"
            
            # Save address for future if checked
            if request.POST.get('save_address') == 'true':
                Address.objects.create(
                    user=request.user,
                    street=street,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    country=country
                )
        
        email = request.POST.get('email', request.user.email)
        phone = request.POST.get('phone', '')
        
        # Verify item stocks before final order placement
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                messages.error(request, f"Insufficient stock for {item.product.name}. Only {item.product.stock} items left.")
                return redirect('cart:detail')
                
        # Generate the Order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            email=email,
            phone=phone,
            total_price=cart.total_price,
            payment_status='Paid'  # Mock instant payment success
        )
        
        # Populate Order Items & Decrement Product Stocks
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            # Update product stock
            product = item.product
            product.stock -= item.quantity
            product.save()
            
        # Clear the Shopping Cart
        cart.items.all().delete()
        
        messages.success(request, "Order placed successfully! Payment approved.")
        return redirect('orders:success', tracking_number=order.tracking_number)
        
    return render(request, 'orders/checkout.html', {'cart': cart, 'addresses': addresses})

@login_required
def order_success_view(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_detail_view(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
