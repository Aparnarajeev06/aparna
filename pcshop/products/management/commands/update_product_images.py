from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Update all trending product images to appropriate files'

    def handle(self, *args, **options):
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
            
            # Memory
            'Corsair Vengeance RGB Pro DDR5 32GB': 'products/corsair_rgb_ram.jpg',
            'G.Skill Trident Z5 RGB DDR5 64GB': 'products/gskill_trident_z5.jpg',
            'Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz': 'products/corsair_rgb_ram.jpg',
            
            # Other
            'ASUS ROG Strix Z790-E Gaming WiFi': 'products/gaming_setup_rgb.jpg',
            'Corsair RM1000x 1000W 80 Plus Gold': 'products/gaming_setup_rgb.jpg',
            'Samsung 990 Pro 2TB NVMe M.2 SSD': 'products/cpu_chip.jpg',
        }

        self.stdout.write(self.style.SUCCESS('\nUPDATING PRODUCT IMAGES\n'))
        updated = 0
        
        for product_name, image_path in image_mapping.items():
            try:
                product = Product.objects.get(name=product_name)
                product.image = image_path
                product.save()
                self.stdout.write(f'  ✓ {product_name}')
                updated += 1
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ✗ Not found: {product_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error: {product_name} - {str(e)[:50]}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Updated {updated} products\n'))
        
        # Show final summary
        self.stdout.write(self.style.SUCCESS('FINAL TRENDING PRODUCTS:\n'))
        trending = Product.objects.filter(is_featured=True).order_by('category__name')
        
        categories = {}
        for product in trending:
            cat = product.category.name
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(product)
        
        for cat in sorted(categories.keys()):
            products = categories[cat]
            self.stdout.write(f'\n{cat} ({len(products)} items):')
            for p in products:
                self.stdout.write(f'  • {p.name}')
                self.stdout.write(f'    └─ {p.image}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ All product images updated successfully!\n'))
