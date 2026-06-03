from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand

class Command(BaseCommand):
    help = 'Add trending CPU products to the database'

    def handle(self, *args, **options):
        # Get or create CPU category
        cpu_category, _ = Category.objects.get_or_create(
            name='Processors',
            defaults={
                'slug': 'processors',
                'icon': 'fa-microchip',
                'description': 'High-performance CPUs for gaming and workstations'
            }
        )

        # Define trending CPUs
        cpus_data = [
            {
                'name': 'Intel Core i9-14900K',
                'brand': 'Intel',
                'price': 589.99,
                'stock': 15,
                'description': 'Flagship 14th gen Intel processor with 24 cores for extreme performance',
                'socket_type': 'LGA1700',
                'wattage': 253,
            },
            {
                'name': 'AMD Ryzen 9 7950X3D',
                'brand': 'AMD',
                'price': 649.99,
                'stock': 12,
                'description': '16-core processor with 3D V-Cache technology for gaming supremacy',
                'socket_type': 'AM5',
                'wattage': 162,
            },
            {
                'name': 'Intel Core i7-14700K',
                'brand': 'Intel',
                'price': 439.99,
                'stock': 20,
                'description': 'High-performance 14th gen processor with 20 cores',
                'socket_type': 'LGA1700',
                'wattage': 253,
            },
            {
                'name': 'AMD Ryzen 7 7700X',
                'brand': 'AMD',
                'price': 329.99,
                'stock': 18,
                'description': '8-core Ryzen processor with excellent single-thread performance',
                'socket_type': 'AM5',
                'wattage': 105,
            },
        ]

        for cpu_data in cpus_data:
            brand_name = cpu_data.pop('brand')
            brand, _ = Brand.objects.get_or_create(name=brand_name)

            product, created = Product.objects.get_or_create(
                name=cpu_data['name'],
                defaults={
                    'category': cpu_category,
                    'brand': brand,
                    'is_featured': True,  # Mark as trending
                    'image': 'products/cpu_chip.jpg',
                    **cpu_data
                }
            )
            
            # Update image for existing products
            if not created and not product.image:
                product.image = 'products/cpu_chip.jpg'
                product.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created trending CPU: {product.name}')
                )
            else:
                # Update existing product to be featured
                product.is_featured = True
                product.save()
                self.stdout.write(
                    self.style.WARNING(f'⚠ Updated existing CPU as trending: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✓ All trending CPUs have been added successfully!')
        )
