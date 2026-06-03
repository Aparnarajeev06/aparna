#!/usr/bin/env python
"""
Helper script to add images to trending products
Run this in the project root: python image_helper.py
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def setup_trending_product_images():
    """Set up image directories and help with image placement"""
    
    media_products = BASE_DIR / 'media' / 'products'
    media_products.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("NOVA TECH PC Shop - Trending Hardware Image Setup")
    print("=" * 60)
    
    print(f"\n✓ Media products directory ready: {media_products}")
    
    print("\n📋 Next Steps:")
    print("-" * 60)
    print("1. Place your CPU chip image in the media/products/ folder")
    print("   Supported formats: PNG, JPG, JPEG, GIF, WEBP")
    print("   Recommended size: 400x400px or larger")
    print("   Filename: cpu_chip.png (or similar)")
    print()
    print("2. Update the add_trending_cpus command with your image filename:")
    print("   Edit: products/management/commands/add_trending_cpus.py")
    print("   Change: 'image': 'products/cpu_placeholder.png'")
    print("   To:     'image': 'products/cpu_chip.png'")
    print()
    print("3. Update existing products:")
    print("   python manage.py shell")
    print("   from products.models import Product")
    print("   p = Product.objects.get(name='Intel Core i9-14900K')")
    print("   p.image = 'products/cpu_chip.png'")
    print("   p.save()")
    print()
    print("4. Check the home page:")
    print("   http://localhost:8000 (Trending Hardware section)")
    print()
    print("-" * 60)
    
    # List existing images
    static_images = BASE_DIR / 'static' / 'images'
    if static_images.exists():
        print("\n📸 Available static images you can use:")
        for img in static_images.glob('*'):
            if img.is_file():
                print(f"   - {img.name}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    setup_trending_product_images()
