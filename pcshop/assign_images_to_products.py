#!/usr/bin/env python
"""
Update trending product images to match their actual products
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

print("\n" + "=" * 80)
print("UPDATING TRENDING PRODUCT IMAGES".center(80))
print("=" * 80 + "\n")

# Image mapping: Product name → Image file
image_mapping = {
    # CPUs
    'Intel Core i9-14900K': 'products/intel_i9_14900k_chip.jpg',
    'AMD Ryzen 9 7950X3D': 'products/cpu_chip.jpg',
    'Intel Core i7-14700K': 'products/cpu_chip.jpg',
    'AMD Ryzen 7 7700X': 'products/cpu_chip.jpg',
    'AMD Ryzen 7 7800X3D': 'products/cpu_chip.jpg',
    
    # GPUs
    'NVIDIA GeForce RTX 4090': 'products/rtx_4090_premium.jpg',
    'MSI GeForce RTX 5060 8G': 'products/msi_rtx_5060.jpg',
    'ASUS TUF GeForce RTX 4080': 'products/asus_rtx_4080.jpg',
    'ASUS ROG Strix NVIDIA RTX 4090 OC 24GB': 'products/rtx_4090_premium.jpg',
    'MSI Gaming X Slim NVIDIA RTX 4070 Ti Super 16GB': 'products/msi_rtx_5060.jpg',
    
    # Laptops
    'ASUS ROG Strix SCAR 18 (RTX 5090)': 'products/asus_rog_strix_scar_18.jpg',
    'ASUS ROG Strix G16 Gaming Laptop': 'products/asus_rog_g16_2024.jpg',
    
    # RAM/Memory
    'Corsair Vengeance RGB Pro DDR5 32GB': 'products/corsair_rgb_ram.jpg',
    'G.Skill Trident Z5 RGB DDR5 64GB': 'products/gskill_trident_z5.jpg',
    'Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz': 'products/corsair_rgb_ram.jpg',
    
    # Generic fallbacks
    'ASUS ROG Strix Z790-E Gaming WiFi': 'products/gaming_setup_rgb.jpg',
    'Corsair RM1000x 1000W 80 Plus Gold': 'products/gaming_setup_rgb.jpg',
    'Samsung 990 Pro 2TB NVMe M.2 SSD': 'products/cpu_chip.jpg',
}

updated_count = 0
failed_count = 0

for product_name, image_path in image_mapping.items():
    try:
        product = Product.objects.get(name=product_name)
        old_image = product.image
        product.image = image_path
        product.save()
        
        if old_image != product.image:
            print(f"✓ Updated: {product_name}")
            print(f"  └─ Image: {image_path}")
            updated_count += 1
        else:
            print(f"→ No change: {product_name}")
    except Product.DoesNotExist:
        print(f"✗ Not found: {product_name}")
        failed_count += 1
    except Exception as e:
        print(f"✗ Error updating {product_name}: {str(e)}")
        failed_count += 1

print("\n" + "=" * 80)
print("UPDATE SUMMARY".center(80))
print("=" * 80)

# Show final status
trending = Product.objects.filter(is_featured=True).order_by('category__name', 'name')

categories = {}
for product in trending:
    cat = product.category.name
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(product)

print(f"\nTotal Products Updated: {updated_count}")
print(f"Total Trending Products: {trending.count()}\n")

for cat in sorted(categories.keys()):
    products = categories[cat]
    print(f"\n{cat.upper()} ({len(products)} products):")
    for p in products:
        img_status = "✓" if p.image else "✗"
        print(f"  {img_status} {p.name}")
        print(f"     Image: {p.image}")

print("\n" + "=" * 80)
print("COMPLETE".center(80))
print("=" * 80 + "\n")
