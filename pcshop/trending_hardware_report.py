#!/usr/bin/env python
"""
Final Trending Hardware Report
Shows all trending products and their images
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

print("\n" + "=" * 80)
print("NOVA TECH PC SHOP - TRENDING HARDWARE FINAL REPORT".center(80))
print("=" * 80 + "\n")

trending = Product.objects.filter(is_featured=True).order_by('category__name', 'name')

print(f"Total Trending Products: {trending.count()}\n")

categories = {}
for product in trending:
    cat = product.category.name
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(product)

for cat in sorted(categories.keys()):
    products = categories[cat]
    print(f"\n{'─' * 80}")
    print(f"{cat.upper()} ({len(products)} products)")
    print(f"{'─' * 80}")
    
    for i, p in enumerate(products, 1):
        img_status = "✓ HAS IMAGE" if p.image else "✗ NO IMAGE"
        print(f"\n  {i}. {p.name}")
        print(f"     Price: ${p.price}")
        print(f"     Brand: {p.brand.name if p.brand else 'N/A'}")
        print(f"     Stock: {p.stock} units")
        print(f"     Image: {img_status}")
        if p.image:
            print(f"            → {p.image}")
        
        # Show specs
        specs = []
        if p.socket_type:
            specs.append(f"Socket: {p.socket_type}")
        if p.ram_type:
            specs.append(f"RAM: {p.ram_type}")
        if p.memory_size:
            specs.append(f"Memory: {p.memory_size}GB")
        if p.storage_type:
            specs.append(f"Storage: {p.storage_type}")
        if p.rgb_support:
            specs.append("RGB: Yes")
        if p.wattage:
            specs.append(f"Power: {p.wattage}W")
        
        if specs:
            print(f"     Specs: {', '.join(specs)}")

print("\n" + "=" * 80)
print("MEDIA FOLDER CONTENTS".center(80))
print("=" * 80 + "\n")

media_path = r'c:\Users\ADMIN\Desktop\aparna\pcshop\media\products'
if os.path.exists(media_path):
    images = os.listdir(media_path)
    print(f"Total images in media/products/: {len(images)}\n")
    for img in sorted(images):
        size = os.path.getsize(os.path.join(media_path, img))
        size_mb = size / (1024 * 1024)
        print(f"  ✓ {img} ({size_mb:.2f} MB)")
else:
    print(f"✗ Media folder not found at {media_path}")

print("\n" + "=" * 80)
print("STATUS: TRENDING HARDWARE SETUP COMPLETE".center(80))
print("=" * 80 + "\n")

print("Next steps:")
print("  1. Visit http://localhost:8000 to view trending hardware")
print("  2. The home page shows up to 6 trending products in the 'Trending Hardware' section")
print("  3. All images are served from /media/products/ directory")
print("  4. Products are marked as 'is_featured=True' in the database\n")
