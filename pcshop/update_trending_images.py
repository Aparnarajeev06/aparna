#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

print("Updating trending products with new images...\n")

# Update ASUS ROG Strix G16 2024
try:
    p = Product.objects.get(name='ASUS ROG Strix G16 Gaming Laptop')
    p.image = 'products/asus_rog_g16_2024.jpg'
    p.save()
    print(f"✓ Updated ASUS ROG Strix G16")
    print(f"  Image: {p.image}\n")
except Product.DoesNotExist:
    print("✗ ASUS ROG Strix G16 Gaming Laptop not found\n")

# Summary of all trending products
print("\nFinal Trending Hardware Inventory:")
print("=" * 60)
trending = Product.objects.filter(is_featured=True).order_by('category__name', 'name')

categories = {}
for product in trending:
    cat = product.category.name
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(product)

for cat in sorted(categories.keys()):
    products = categories[cat]
    print(f"\n{cat} ({len(products)} items):")
    for p in products:
        img_status = "✓" if p.image else "✗"
        print(f"  {img_status} {p.name}")
        if p.image:
            print(f"    └─ {p.image}")

print(f"\n{'=' * 60}")
print(f"Total Trending Products: {trending.count()}")
