from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Category, Brand, Product, Wishlist, Review
from orders.models import Order, OrderItem
from django.contrib.auth.models import User

def home_view(request):
    featured_categories = Category.objects.all()[:6]
    trending_products = Product.objects.filter(is_featured=True)[:6]
    # Fetch RTX card if exists for the promo banner
    rtx_promo = Product.objects.filter(name__icontains="4090").first()
    context = {
        "featured_categories": featured_categories,
        "trending_products": trending_products,
        "rtx_promo": rtx_promo
    }
    return render(request, "products/home.html", context)

def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # Capture Query Parameters
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    brand_slug = request.GET.get('brand', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    rgb = request.GET.get('rgb', '')
    socket = request.GET.get('socket', '')
    ram = request.GET.get('ram', '')
    storage = request.GET.get('storage', '')

    # Apply Search Filter
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(brand__name__icontains=query)
        )

    # Apply Category & Brand Filters
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Apply Price Range
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Technical Spec Filters
    if rgb == 'yes':
        products = products.filter(rgb_support=True)
    elif rgb == 'no':
        products = products.filter(rgb_support=False)

    if socket:
        products = products.filter(socket_type__iexact=socket)
    
    if ram:
        products = products.filter(ram_type__iexact=ram)

    if storage:
        products = products.filter(storage_type__iexact=storage)

    # Unique specifications for filter options
    socket_types = Product.objects.exclude(socket_type='').values_list('socket_type', flat=True).distinct()
    ram_types = Product.objects.exclude(ram_type='').values_list('ram_type', flat=True).distinct()
    storage_types = Product.objects.exclude(storage_type='').values_list('storage_type', flat=True).distinct()

    context = {
        "products": products,
        "categories": categories,
        "brands": brands,
        "socket_types": socket_types,
        "ram_types": ram_types,
        "storage_types": storage_types,
        "params": request.GET
    }
    return render(request, "products/product_list.html", context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by("-created_at")
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Check if this item is in the user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    context = {
        "product": product,
        "reviews": reviews,
        "related_products": related_products,
        "in_wishlist": in_wishlist
    }
    return render(request, "products/product_detail.html", context)

@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")
        if rating:
            Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={"rating": int(rating), "comment": comment}
            )
            messages.success(request, "Thank you! Your hardware review has been submitted.")
        else:
            messages.error(request, "Please provide a rating standard.")
    return redirect("products:detail", slug=product.slug)

@login_required
def toggle_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        messages.success(request, f"{product.name} removed from your Wishlist.")
    else:
        messages.success(request, f"{product.name} added to your Wishlist.")
    
    # Return to details or lists
    next_url = request.GET.get('next', 'products:detail')
    if next_url == 'products:list':
        return redirect('products:list')
    return redirect('products:detail', slug=product.slug)

def live_search_view(request):
    query = request.GET.get('term', '')
    results = []
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(brand__name__icontains=query)
        )[:6]
        for p in products:
            results.append({
                "label": p.name,
                "value": p.name,
                "slug": p.slug,
                "price": str(p.price),
                "image": p.image_url
            })
    return JsonResponse(results, safe=False)

@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def admin_dashboard_view(request):
    total_revenue = Order.objects.filter(payment_status="Paid").aggregate(sum_rev=Sum("total_price"))["sum_rev"] or 0
    total_orders = Order.objects.count()
    low_stock_products = Product.objects.filter(stock__lte=5)
    total_users = User.objects.count()
    recent_orders = Order.objects.all().order_by("-created_at")[:10]
    all_products = Product.objects.all()

    context = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "low_stock_products": low_stock_products,
        "total_users": total_users,
        "recent_orders": recent_orders,
        "all_products": all_products
    }
    return render(request, "products/admin_dashboard.html", context)
