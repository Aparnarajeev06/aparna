from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from products.models import Product, Category
from cart.views import get_or_create_cart
from cart.models import CartItem
from .models import PCBuild

def get_user_build(request):
    if request.user.is_authenticated:
        build, created = PCBuild.objects.get_or_create(user=request.user, name="My Active Rig")
        
        # Merge guest build if exists
        guest_build_id = request.session.get('active_build_id')
        if guest_build_id:
            guest_build = PCBuild.objects.filter(id=guest_build_id).first()
            if guest_build:
                build.cpu = build.cpu or guest_build.cpu
                build.motherboard = build.motherboard or guest_build.motherboard
                build.ram = build.ram or guest_build.ram
                build.gpu = build.gpu or guest_build.gpu
                build.storage = build.storage or guest_build.storage
                build.psu = build.psu or guest_build.psu
                build.save()
                guest_build.delete()
                del request.session['active_build_id']
    else:
        build_id = request.session.get('active_build_id')
        build = None
        if build_id:
            build = PCBuild.objects.filter(id=build_id).first()
        if not build:
            build = PCBuild.objects.create(name="Active Guest Build")
            request.session['active_build_id'] = build.id
            
    return build

def pc_builder_view(request):
    build = get_user_build(request)
    
    # Calculate statistics
    total_price = build.total_price
    total_wattage = build.total_wattage
    
    # Check compatibilities and build detailed warning messages
    warnings = []
    
    # Socket compatibility check
    if build.cpu and build.motherboard:
        if build.cpu.socket_type.lower() != build.motherboard.socket_type.lower():
            warnings.append(f"⚠️ SOCKET MISMATCH: Your CPU ({build.cpu.name}) uses socket '{build.cpu.socket_type}', but your Motherboard ({build.motherboard.name}) is built for socket '{build.motherboard.socket_type}'.")
            
    # RAM standard check
    if build.motherboard and build.ram:
        if build.motherboard.ram_type.lower() != build.ram.ram_type.lower():
            warnings.append(f"⚠️ MEMORY TYPE MISMATCH: Your Motherboard ({build.motherboard.name}) supports '{build.motherboard.ram_type}' RAM, but your chosen RAM ({build.ram.name}) is '{build.ram.ram_type}'.")
            
    # Wattage capacities check
    if build.psu and total_wattage > 0:
        if total_wattage > build.psu.wattage:
            warnings.append(f"⚠️ PSU CAPACITY CRITICAL: Your parts require ~{total_wattage}W of power, but your Power Supply unit ({build.psu.name}) is rated for only {build.psu.wattage}W.")
        elif total_wattage > (build.psu.wattage * 0.85):
            warnings.append(f"⚠️ PSU CAPACITY WARN: Your parts require ~{total_wattage}W. To maintain efficiency and safe power overhead, we recommend a Power Supply with at least {int(total_wattage * 1.25)}W capacity.")

    context = {
        'build': build,
        'total_price': total_price,
        'total_wattage': total_wattage,
        'warnings': warnings,
        'is_compatible': len(warnings) == 0
    }
    return render(request, 'builder/pc_builder.html', context)

def select_part_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    build = get_user_build(request)

    # Filter parts for compatibility dynamically to be extra helpful!
    compatibility_filter = request.GET.get('compatible_only', 'false') == 'true'
    
    if compatibility_filter:
        if category_slug == 'motherboards' and build.cpu:
            products = products.filter(socket_type__iexact=build.cpu.socket_type)
        elif category_slug == 'cpus' and build.motherboard:
            products = products.filter(socket_type__iexact=build.motherboard.socket_type)
        elif category_slug == 'ram' and build.motherboard:
            products = products.filter(ram_type__iexact=build.motherboard.ram_type)
            
    context = {
        'category': category,
        'products': products,
        'build': build,
        'compatible_only': compatibility_filter
    }
    return render(request, 'builder/select_part.html', context)

def add_part_to_build_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    build = get_user_build(request)
    category_slug = product.category.slug
    
    if category_slug == 'cpus':
        build.cpu = product
    elif category_slug == 'motherboards':
        build.motherboard = product
    elif category_slug == 'ram':
        build.ram = product
    elif category_slug == 'gpus':
        build.gpu = product
    elif category_slug == 'storage':
        build.storage = product
    elif category_slug == 'power-supplies':
        build.psu = product
    else:
        messages.error(request, "This product category is not supported inside the custom PC builder.")
        return redirect('builder:configurator')
        
    build.save()
    messages.success(request, f"{product.name} locked into your rig setup.")
    return redirect('builder:configurator')

def remove_part_from_build_view(request, part_type):
    build = get_user_build(request)
    
    if part_type == 'cpu':
        build.cpu = None
    elif part_type == 'motherboard':
        build.motherboard = None
    elif part_type == 'ram':
        build.ram = None
    elif part_type == 'gpu':
        build.gpu = None
    elif part_type == 'storage':
        build.storage = None
    elif part_type == 'psu':
        build.psu = None
        
    build.save()
    messages.success(request, f"Cleared {part_type.upper()} selection.")
    return redirect('builder:configurator')

def add_build_to_cart_view(request):
    build = get_user_build(request)
    cart = get_or_create_cart(request)
    
    added_count = 0
    components = [build.cpu, build.motherboard, build.ram, build.gpu, build.storage, build.psu]
    
    for part in components:
        if part:
            if part.stock > 0:
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=part)
                if not created:
                    cart_item.quantity += 1
                cart_item.save()
                added_count += 1
            else:
                messages.warning(request, f"Skipped adding {part.name} (Out of stock).")
                
    if added_count > 0:
        messages.success(request, f"Loaded {added_count} parts of your custom rig into your Shopping Cart!")
    else:
        messages.error(request, "Your active build is empty! Build a rig first.")
        
    return redirect('cart:detail')

def ai_recommendation_view(request):
    budget_tier = request.GET.get('budget', 'mid')
    primary_use = request.GET.get('usecase', 'gaming')
    
    # Define budget values
    # low: < $800, mid: $800 - $1600, high: > $1600
    
    # Query database and build a compatible mockup setup
    cpu = None
    motherboard = None
    ram = None
    gpu = None
    storage = None
    psu = None
    
    if budget_tier == 'low':
        # Budget components
        cpu = Product.objects.filter(category__slug='cpus', price__lte=220).order_by('price').first()
        ram = Product.objects.filter(category__slug='ram', ram_type='DDR4').first()
        motherboard = Product.objects.filter(category__slug='motherboards', ram_type='DDR4').first()
        gpu = Product.objects.filter(category__slug='gpus', price__lte=550).first()
        storage = Product.objects.filter(category__slug='storage', storage_type='SATA SSD').first()
        psu = Product.objects.filter(category__slug='power-supplies', wattage__lte=750).first()
    elif budget_tier == 'high':
        # Premium hardware
        cpu = Product.objects.filter(category__slug='cpus', name__icontains='14900K').first() or Product.objects.filter(category__slug='cpus').order_by('-price').first()
        motherboard = Product.objects.filter(category__slug='motherboards', name__icontains='Z790').first() or Product.objects.filter(category__slug='motherboards').order_by('-price').first()
        ram = Product.objects.filter(category__slug='ram', ram_type='DDR5').order_by('-price').first()
        gpu = Product.objects.filter(category__slug='gpus', name__icontains='4090').first() or Product.objects.filter(category__slug='gpus').order_by('-price').first()
        storage = Product.objects.filter(category__slug='storage', name__icontains='990 Pro').first() or Product.objects.filter(category__slug='storage').order_by('-price').first()
        psu = Product.objects.filter(category__slug='power-supplies', wattage__gte=1000).first()
    else:
        # Mid-range hardware
        cpu = Product.objects.filter(category__slug='cpus', name__icontains='7800X3D').first() or Product.objects.filter(category__slug='cpus').filter(price__range=(200, 450)).first()
        motherboard = Product.objects.filter(category__slug='motherboards', name__icontains='B650').first() or Product.objects.filter(category__slug='motherboards').filter(price__range=(150, 300)).first()
        ram = Product.objects.filter(category__slug='ram', ram_type='DDR5').filter(price__lte=130).first()
        gpu = Product.objects.filter(category__slug='gpus', name__icontains='4070').first() or Product.objects.filter(category__slug='gpus').filter(price__range=(400, 900)).first()
        storage = Product.objects.filter(category__slug='storage', name__icontains='990 Pro').first() or Product.objects.filter(category__slug='storage').first()
        psu = Product.objects.filter(category__slug='power-supplies', wattage__gte=750).first()

    recommended_components = [cpu, motherboard, ram, gpu, storage, psu]
    valid_components = [c for c in recommended_components if c is not None]
    total_price = sum(c.price for c in valid_components)
    total_wattage = sum(c.wattage for c in valid_components if c.category.slug in ['cpus', 'gpus', 'ram', 'storage'])

    # Handle loading the recommendation into active configuration
    load_build = request.GET.get('load', 'false') == 'true'
    if load_build:
        build = get_user_build(request)
        build.cpu = cpu
        build.motherboard = motherboard
        build.ram = ram
        build.gpu = gpu
        build.storage = storage
        build.psu = psu
        build.save()
        messages.success(request, f"Loaded AI Recommended {budget_tier.capitalize()} configuration into your PC Builder!")
        return redirect('builder:configurator')

    context = {
        'cpu': cpu,
        'motherboard': motherboard,
        'ram': ram,
        'gpu': gpu,
        'storage': storage,
        'psu': psu,
        'total_price': total_price,
        'total_wattage': total_wattage,
        'budget': budget_tier,
        'usecase': primary_use
    }
    return render(request, 'builder/ai_recommendations.html', context)
