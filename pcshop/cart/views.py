from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    
    if request.user.is_authenticated:
        # User is logged in. Get or create user cart.
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if there is an anonymous session cart to merge
        session_cart = Cart.objects.filter(session_key=session_key).first()
        if session_cart:
            # Merge items
            for item in session_cart.items.all():
                # Check if item already exists in user cart
                existing_item = user_cart.items.filter(product=item.product).first()
                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    item.cart = user_cart
                    item.save()
            # Delete the session cart
            session_cart.delete()
            
        return user_cart
    else:
        # User is guest. Get or create session-based cart.
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

def cart_detail_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if quantity exceeds stock
    if product.stock == 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock!")
        return redirect('products:detail', slug=product.slug)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        new_qty = cart_item.quantity + quantity
        if new_qty > product.stock:
            cart_item.quantity = product.stock
            messages.warning(request, f"Limited stock available. Cart updated to maximum available stock ({product.stock}).")
        else:
            cart_item.quantity = new_qty
            messages.success(request, f"Added {quantity} x {product.name} to your Cart.")
    else:
        if quantity > product.stock:
            cart_item.quantity = product.stock
            messages.warning(request, f"Limited stock available. Cart updated to maximum available stock ({product.stock}).")
        else:
            cart_item.quantity = quantity
            messages.success(request, f"Added {product.name} to your Cart.")
            
    cart_item.save()
    
    next_url = request.GET.get('next', 'cart:detail')
    if next_url == 'products:list':
        return redirect('products:list')
    return redirect('cart:detail')

def update_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, f"Removed {product.name} from Cart.")
        else:
            if quantity > product.stock:
                cart_item.quantity = product.stock
                messages.warning(request, f"Only {product.stock} units of {product.name} are in stock.")
            else:
                cart_item.quantity = quantity
                messages.success(request, "Cart quantity updated.")
            cart_item.save()
            
    return redirect('cart:detail')

def remove_from_cart_view(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    messages.success(request, f"Removed {product.name} from your Cart.")
    return redirect('cart:detail')
