import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from products.models import Product

image_mapping = {
    'Intel Core i9-14900K': 'products/intel_i9_14900k_chip.jpg',
    'AMD Ryzen 9 7950X3D': 'products/cpu_chip.jpg',
    'Intel Core i7-14700K': 'products/cpu_chip.jpg',
    'AMD Ryzen 7 7700X': 'products/cpu_chip.jpg',
    'AMD Ryzen 7 7800X3D': 'products/cpu_chip.jpg',
    'NVIDIA GeForce RTX 4090': 'products/rtx_4090_premium.jpg',
    'MSI GeForce RTX 5060 8G': 'products/msi_rtx_5060.jpg',
    'ASUS TUF GeForce RTX 4080': 'products/asus_rtx_4080.jpg',
    'ASUS ROG Strix NVIDIA RTX 4090 OC 24GB': 'products/rtx_4090_premium.jpg',
    'MSI Gaming X Slim NVIDIA RTX 4070 Ti Super 16GB': 'products/msi_rtx_5060.jpg',
    'ASUS ROG Strix SCAR 18 (RTX 5090)': 'products/asus_rog_strix_scar_18.jpg',
    'ASUS ROG Strix G16 Gaming Laptop': 'products/asus_rog_g16_2024.jpg',
    'Corsair Vengeance RGB Pro DDR5 32GB': 'products/corsair_rgb_ram.jpg',
    'G.Skill Trident Z5 RGB DDR5 64GB': 'products/gskill_trident_z5.jpg',
    'Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz': 'products/corsair_rgb_ram.jpg',
    'ASUS ROG Strix Z790-E Gaming WiFi': 'products/gaming_setup_rgb.jpg',
    'Corsair RM1000x 1000W 80 Plus Gold': 'products/gaming_setup_rgb.jpg',
    'Samsung 990 Pro 2TB NVMe M.2 SSD': 'products/cpu_chip.jpg',
}

output = []
output.append('UPDATING PRODUCT IMAGES\n')
updated = 0
for product_name, image_path in image_mapping.items():
    try:
        product = Product.objects.get(name=product_name)
        product.image = image_path
        product.save()
        output.append(f'OK: {product_name}')
        updated += 1
    except Exception as e:
        output.append(f'SKIP: {product_name} - {str(e)[:50]}')

output.append(f'\nUpdated {updated} products')
output.append('\n' + '='*60)
output.append('FINAL TRENDING PRODUCTS')
output.append('='*60 + '\n')

trending = Product.objects.filter(is_featured=True).order_by('category__name')
for p in trending:
    output.append(f'{p.category.name}: {p.name}')
    output.append(f'  Image: {p.image}\n')

# Write to file
with open('update_results.txt', 'w') as f:
    f.write('\n'.join(output))

print("Complete - check update_results.txt")
