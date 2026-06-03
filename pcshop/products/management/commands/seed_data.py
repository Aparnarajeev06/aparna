from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Brand, Product
from support.models import FAQ

class Command(BaseCommand):
    help = "Seeds categories, brands, products, and FAQs into the database"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # 1. Seed Categories
        categories_data = [
            {"name": "CPUs", "icon": "fa-microchip", "description": "High-performance central processors from Intel and AMD."},
            {"name": "GPUs", "icon": "fa-gamepad", "description": "Graphics cards for extreme gaming and visual rendering."},
            {"name": "RAM", "icon": "fa-memory", "description": "High-speed system memory modules for multitasking."},
            {"name": "Motherboards", "icon": "fa-server", "description": "Central circuit boards for sockets and memory components."},
            {"name": "Storage", "icon": "fa-hdd", "description": "NVMe M.2 and SATA solid-state drives."},
            {"name": "Power Supplies", "icon": "fa-plug", "description": "Energy efficient ATX power supplies for power distribution."}
        ]

        categories = {}
        for cat in categories_data:
            obj, created = Category.objects.get_or_create(
                name=cat["name"],
                defaults={"icon": cat["icon"], "description": cat["description"]}
            )
            categories[cat["name"]] = obj
            if created:
                self.stdout.write(f"Created category: {cat['name']}")

        # 2. Seed Brands
        brands_data = ["Intel", "AMD", "NVIDIA", "ASUS", "MSI", "Corsair", "Samsung", "G.Skill", "EVGA"]
        brands = {}
        for br in brands_data:
            obj, created = Brand.objects.get_or_create(name=br)
            brands[br] = obj
            if created:
                self.stdout.write(f"Created brand: {br}")

        # 3. Seed Products
        products_data = [
            # CPUs
            {
                "name": "Intel Core i9-14900K",
                "description": "24-Core desktop processor with Max Turbo Speed of 6.0 GHz, LGA1700 Socket, DDR5 support. Extreme power for gamers and creators.",
                "image": "https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=600&auto=format&fit=crop",
                "price": 589.99,
                "stock": 15,
                "brand": brands["Intel"],
                "category": categories["CPUs"],
                "is_featured": True,
                "socket_type": "LGA1700",
                "ram_type": "DDR5",
                "wattage": 125,
                "rgb_support": False
            },
            {
                "name": "AMD Ryzen 7 7800X3D",
                "description": "8-Core desktop processor featuring AMD 3D V-Cache technology for exceptional 1085p gaming performance, AM5 Socket, DDR5 support.",
                "image": "https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=600&auto=format&fit=crop",
                "price": 389.99,
                "stock": 20,
                "brand": brands["AMD"],
                "category": categories["CPUs"],
                "is_featured": True,
                "socket_type": "AM5",
                "ram_type": "DDR5",
                "wattage": 120,
                "rgb_support": False
            },
            {
                "name": "Intel Core i5-13400F",
                "description": "10-Core budget desktop processor with Max Turbo Speed of 4.6 GHz, LGA1700 Socket, DDR4 & DDR5 support (configured for DDR4 setups).",
                "image": "https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=600&auto=format&fit=crop",
                "price": 199.99,
                "stock": 30,
                "brand": brands["Intel"],
                "category": categories["CPUs"],
                "is_featured": False,
                "socket_type": "LGA1700",
                "ram_type": "DDR4",
                "wattage": 65,
                "rgb_support": False
            },
            # Motherboards
            {
                "name": "ASUS ROG Strix Z790-E Gaming WiFi",
                "description": "High-end Intel LGA1700 ATX motherboard, features PCIe 5.0, robust power delivery, DDR5 memory slots, on-board RGB highlights, and WiFi 6E.",
                "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=600&auto=format&fit=crop",
                "price": 429.99,
                "stock": 10,
                "brand": brands["ASUS"],
                "category": categories["Motherboards"],
                "is_featured": True,
                "socket_type": "LGA1700",
                "ram_type": "DDR5",
                "wattage": 60,
                "rgb_support": True
            },
            {
                "name": "MSI MAG B650 Tomahawk WiFi",
                "description": "Sleek and robust AMD AM5 ATX motherboard, designed for AMD Ryzen 7000/8000 series, DDR5 RAM lanes, lightning Gen 4 M.2 slots, and premium audio.",
                "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=600&auto=format&fit=crop",
                "price": 219.99,
                "stock": 18,
                "brand": brands["MSI"],
                "category": categories["Motherboards"],
                "is_featured": False,
                "socket_type": "AM5",
                "ram_type": "DDR5",
                "wattage": 50,
                "rgb_support": False
            },
            {
                "name": "ASUS TUF Gaming B660M-PLUS D4",
                "description": "Micro-ATX Intel LGA1700 motherboard, built with military-grade components, supporting DDR4 memory, PCIe 4.0, M.2 slots, and Aura Sync RGB.",
                "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=600&auto=format&fit=crop",
                "price": 139.99,
                "stock": 25,
                "brand": brands["ASUS"],
                "category": categories["Motherboards"],
                "is_featured": False,
                "socket_type": "LGA1700",
                "ram_type": "DDR4",
                "wattage": 45,
                "rgb_support": True
            },
            # RAM
            {
                "name": "Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz",
                "description": "High-performance Corsair DDR5 RAM kit. Dynamic multi-zone RGB lighting, optimized for Intel and AMD DDR5 platforms.",
                "image": "https://images.unsplash.com/photo-1562976540-1502c2145186?q=80&w=600&auto=format&fit=crop",
                "price": 114.99,
                "stock": 40,
                "brand": brands["Corsair"],
                "category": categories["RAM"],
                "is_featured": True,
                "ram_type": "DDR5",
                "memory_size": 32,
                "wattage": 10,
                "rgb_support": True
            },
            {
                "name": "G.Skill Ripjaws V 16GB (2x8GB) DDR4 3200MHz",
                "description": "Standard high-reliability DDR4 system memory kit. Sleek aluminum heatspreader, excellent for multitasking and budget builds.",
                "image": "https://images.unsplash.com/photo-1562976540-1502c2145186?q=80&w=600&auto=format&fit=crop",
                "price": 44.99,
                "stock": 50,
                "brand": brands["G.Skill"],
                "category": categories["RAM"],
                "is_featured": False,
                "ram_type": "DDR4",
                "memory_size": 16,
                "wattage": 8,
                "rgb_support": False
            },
            # GPUs
            {
                "name": "ASUS ROG Strix NVIDIA RTX 4090 OC 24GB",
                "description": "The ultimate gaming graphics card. Powered by NVIDIA Ada Lovelace architecture, featuring 24GB G6X VRAM, DLSS 3, and high-wattage custom cooling.",
                "image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=600&auto=format&fit=crop",
                "price": 1999.99,
                "stock": 5,
                "brand": brands["ASUS"],
                "category": categories["GPUs"],
                "is_featured": True,
                "memory_size": 24,
                "wattage": 450,
                "rgb_support": True
            },
            {
                "name": "MSI Gaming X Slim NVIDIA RTX 4070 Ti Super 16GB",
                "description": "Slim form factor RTX 4070 Ti Super. Offers 16GB VRAM, premium cooling, dual bios, custom RGB accents, and amazing 1440p / 4K gaming frames.",
                "image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=600&auto=format&fit=crop",
                "price": 849.99,
                "stock": 12,
                "brand": brands["MSI"],
                "category": categories["GPUs"],
                "is_featured": True,
                "memory_size": 16,
                "wattage": 285,
                "rgb_support": True
            },
            {
                "name": "Sapphire Pulse AMD Radeon RX 7800 XT 16GB",
                "description": "Exceptional value graphics card. 16GB VRAM, dual-axial cooling fans, metal backplate, great raw compute capability, and robust software controls.",
                "image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=600&auto=format&fit=crop",
                "price": 499.99,
                "stock": 15,
                "brand": brands["AMD"],
                "category": categories["GPUs"],
                "is_featured": False,
                "memory_size": 16,
                "wattage": 263,
                "rgb_support": False
            },
            # Storage
            {
                "name": "Samsung 990 Pro 2TB NVMe M.2 SSD",
                "description": "Blazing fast PCIe Gen 4.0 NVMe SSD. Sequential read speeds up to 7450 MB/s, sequential write speeds up to 6900 MB/s. Perfect load times.",
                "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?q=80&w=600&auto=format&fit=crop",
                "price": 179.99,
                "stock": 25,
                "brand": brands["Samsung"],
                "category": categories["Storage"],
                "is_featured": True,
                "storage_type": "NVMe M.2 SSD",
                "wattage": 6,
                "rgb_support": False
            },
            {
                "name": "Crucial MX500 1TB SATA 2.5 Inch SSD",
                "description": "Reliable 2.5 inch SATA solid state drive. Read speeds up to 560 MB/s, great for secondary storage of large gaming libraries.",
                "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?q=80&w=600&auto=format&fit=crop",
                "price": 79.99,
                "stock": 35,
                "brand": brands["Corsair"], # fallback brand
                "category": categories["Storage"],
                "is_featured": False,
                "storage_type": "SATA SSD",
                "wattage": 4,
                "rgb_support": False
            },
            # Power Supplies
            {
                "name": "Corsair RM1000x 1000W 80 Plus Gold",
                "description": "1000W fully modular ATX power supply. 80 PLUS Gold certified, zero RPM fan mode, 100% Japanese 105C electrolytic capacitors. Perfect for multi-GPU setups.",
                "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?q=80&w=600&auto=format&fit=crop",
                "price": 189.99,
                "stock": 14,
                "brand": brands["Corsair"],
                "category": categories["Power Supplies"],
                "is_featured": True,
                "wattage": 1000,
                "rgb_support": False
            },
            {
                "name": "EVGA SuperNOVA 750 GT 750W 80 Plus Gold",
                "description": "750W fully modular power supply. 80 PLUS Gold certified, compact size, auto ECO mode for silent operation. Ideal for single high-end GPU builds.",
                "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?q=80&w=600&auto=format&fit=crop",
                "price": 119.99,
                "stock": 20,
                "brand": brands["EVGA"],
                "category": categories["Power Supplies"],
                "is_featured": False,
                "wattage": 750,
                "rgb_support": False
            }
        ]

        for p_data in products_data:
            obj, created = Product.objects.get_or_create(
                name=p_data["name"],
                defaults={
                    "slug": slugify(p_data["name"]),
                    "description": p_data["description"],
                    "image": p_data["image"],
                    "price": p_data["price"],
                    "stock": p_data["stock"],
                    "brand": p_data["brand"],
                    "category": p_data["category"],
                    "is_featured": p_data["is_featured"],
                    "socket_type": p_data.get("socket_type", ""),
                    "ram_type": p_data.get("ram_type", ""),
                    "memory_size": p_data.get("memory_size", None),
                    "storage_type": p_data.get("storage_type", ""),
                    "rgb_support": p_data.get("rgb_support", False),
                    "wattage": p_data.get("wattage", 0),
                }
            )
            if created:
                self.stdout.write(f"Created product: {p_data['name']}")

        # 4. Seed FAQs
        faqs_data = [
            {
                "question": "How does the PC Builder compatibility checking work?",
                "answer": "Our PC Builder checks two primary requirements: first, that your selected CPU socket type matches your Motherboard's CPU socket type (e.g. LGA1700 or AM5). Second, it verifies that your chosen RAM DDR generation (DDR4 or DDR5) matches the RAM slots of the Motherboard. It also calculates the total wattage requirements of your active components and checks them against your PSU capacity.",
                "category": "Hardware"
            },
            {
                "question": "What is the return/warranty policy on PC parts?",
                "answer": "All PC parts sold on NOVA TECH carry a 30-day money-back satisfaction warranty. Defective components can be returned for a replacement or store credit. You can initiate a Return Merchandise Authorization (RMA) ticket directly from your User Dashboard inside the order details tab.",
                "category": "General"
            },
            {
                "question": "How long does shipping take?",
                "answer": "Standard shipping takes 3-5 business days. Premium gaming express shipping takes 1-2 business days. Tracking details will be generated immediately in your Orders Panel when the order transitions to 'Shipped'.",
                "category": "Shipping"
            },
            {
                "question": "What payment methods do you support?",
                "answer": "We support major credit cards (Visa, MasterCard, Amex), PayPal, and cryptocurrencies like Bitcoin (BTC) and Ethereum (ETH) for gamers and tech enthusiasts.",
                "category": "Billing"
            }
        ]

        for f_data in faqs_data:
            obj, created = FAQ.objects.get_or_create(
                question=f_data["question"],
                defaults={"answer": f_data["answer"], "category": f_data["category"]}
            )
            if created:
                self.stdout.write(f"Created FAQ: {f_data['question']}")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
