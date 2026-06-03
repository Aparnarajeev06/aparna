from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand

class Command(BaseCommand):
    help = 'Add trending GPU and other hardware products to the database'

    def handle(self, *args, **options):
        # Get or create categories
        gpu_category, _ = Category.objects.get_or_create(
            name='Graphics Cards',
            defaults={
                'slug': 'graphics-cards',
                'icon': 'fa-video',
                'description': 'High-performance GPUs for gaming and workstations'
            }
        )

        ram_category, _ = Category.objects.get_or_create(
            name='Memory',
            defaults={
                'slug': 'memory',
                'icon': 'fa-memory',
                'description': 'Fast DDR4 and DDR5 RAM modules'
            }
        )

        # Define trending GPUs
        gpus_data = [
            {
                'name': 'MSI GeForce RTX 5060 8G',
                'brand': 'MSI',
                'price': 299.99,
                'stock': 10,
                'description': 'High-performance graphics card with 8GB GDDR6 memory, perfect for 1440p gaming',
                'memory_size': 8,
                'storage_type': 'GDDR6',
                'rgb_support': True,
                'wattage': 170,
                'image': 'products/msi_rtx_5060.jpg',
            },
            {
                'name': 'NVIDIA GeForce RTX 4090',
                'brand': 'NVIDIA',
                'price': 1599.99,
                'stock': 5,
                'description': 'Ultimate gaming GPU - RTX 4090 with 24GB GDDR6X memory, extreme performance',
                'memory_size': 24,
                'storage_type': 'GDDR6X',
                'rgb_support': True,
                'wattage': 450,
                'image': 'products/rtx_4090.jpg',
            },
            {
                'name': 'ASUS TUF GeForce RTX 4080',
                'brand': 'ASUS',
                'price': 1199.99,
                'stock': 8,
                'description': 'Premium gaming GPU with advanced cooling, 16GB GDDR6X memory',
                'memory_size': 16,
                'storage_type': 'GDDR6X',
                'rgb_support': True,
                'wattage': 320,
                'image': 'products/asus_rtx_4080.jpg',
            },
        ]

        # Define trending RAM
        ram_data = [
            {
                'name': 'Corsair Vengeance RGB Pro DDR5 32GB',
                'brand': 'Corsair',
                'price': 189.99,
                'stock': 15,
                'description': 'Premium DDR5 RAM with dynamic RGB lighting, 32GB capacity for ultimate multitasking',
                'ram_type': 'DDR5',
                'memory_size': 32,
                'rgb_support': True,
                'wattage': 10,
                'image': 'products/corsair_rgb_ram.jpg',
            },
            {
                'name': 'G.Skill Trident Z5 RGB DDR5 64GB',
                'brand': 'G.Skill',
                'price': 349.99,
                'stock': 12,
                'description': 'Ultra-high capacity DDR5 RAM with RGB support, 64GB for extreme workstations',
                'ram_type': 'DDR5',
                'memory_size': 64,
                'rgb_support': True,
                'wattage': 12,
                'image': 'products/gskill_trident_z5.jpg',
            },
        ]

        # Process GPUs
        for gpu_data in gpus_data:
            brand_name = gpu_data.pop('brand')
            image = gpu_data.pop('image')
            brand, _ = Brand.objects.get_or_create(name=brand_name)

            product, created = Product.objects.get_or_create(
                name=gpu_data['name'],
                defaults={
                    'category': gpu_category,
                    'brand': brand,
                    'is_featured': True,
                    'image': image,
                    **gpu_data
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created trending GPU: {product.name}')
                )
            else:
                product.is_featured = True
                product.image = image
                product.save()
                self.stdout.write(
                    self.style.WARNING(f'⚠ Updated GPU as trending: {product.name}')
                )

        # Process RAM
        for ram_info in ram_data:
            brand_name = ram_info.pop('brand')
            image = ram_info.pop('image')
            brand, _ = Brand.objects.get_or_create(name=brand_name)

            product, created = Product.objects.get_or_create(
                name=ram_info['name'],
                defaults={
                    'category': ram_category,
                    'brand': brand,
                    'is_featured': True,
                    'image': image,
                    **ram_info
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created trending RAM: {product.name}')
                )
            else:
                product.is_featured = True
                product.image = image
                product.save()
                self.stdout.write(
                    self.style.WARNING(f'⚠ Updated RAM as trending: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✓ All trending GPUs and RAM have been added successfully!')
        )
