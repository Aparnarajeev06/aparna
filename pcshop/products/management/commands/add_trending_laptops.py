from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand

class Command(BaseCommand):
    help = 'Add trending laptop products to the database'

    def handle(self, *args, **options):
        # Get or create Laptops category
        laptop_category, created = Category.objects.get_or_create(
            name='Laptops',
            defaults={
                'slug': 'laptops',
                'icon': 'fa-laptop',
                'description': 'High-performance gaming and workstation laptops'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Laptops category'))

        # Define trending laptops
        laptops_data = [
            {
                'name': 'ASUS ROG Strix SCAR 18 (RTX 5090)',
                'brand': 'ASUS',
                'price': 4299.99,
                'stock': 3,
                'description': "World's most powerful laptop with RTX 5090, Intel Core i9, 18\" display",
                'memory_size': 32,
                'ram_type': 'DDR5',
                'storage_type': 'NVMe M.2 SSD',
                'rgb_support': True,
                'wattage': 280,
                'image': 'products/asus_rog_strix_scar_18.jpg',
            },
            {
                'name': 'ASUS ROG Strix G16 Gaming Laptop',
                'brand': 'ASUS',
                'price': 1999.99,
                'stock': 5,
                'description': 'Premium gaming laptop with RTX 4060, Intel Core i9-13980HX, 16" 165Hz display',
                'memory_size': 16,
                'ram_type': 'DDR5',
                'storage_type': 'NVMe M.2 SSD',
                'rgb_support': True,
                'wattage': 240,
                'image': 'products/asus_rog_strix_g16.jpg',
            },
        ]

        # Process laptops
        for laptop_data in laptops_data:
            brand_name = laptop_data.pop('brand')
            image = laptop_data.pop('image')
            brand, _ = Brand.objects.get_or_create(name=brand_name)

            product, created = Product.objects.get_or_create(
                name=laptop_data['name'],
                defaults={
                    'category': laptop_category,
                    'brand': brand,
                    'is_featured': True,
                    'image': image,
                    **laptop_data
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created trending laptop: {product.name}')
                )
            else:
                product.is_featured = True
                product.image = image
                product.save()
                self.stdout.write(
                    self.style.WARNING(f'⚠ Updated laptop as trending: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✓ All trending laptops have been added successfully!')
        )
