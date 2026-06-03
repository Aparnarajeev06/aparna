# Adding Trending Hardware Images to NOVA TECH PC Shop

## Step 1: Add Your CPU Image to Media Folder

1. Copy the circuit board/CPU image you provided to:
   ```
   pcshop/media/products/trending_cpu_chip.png
   ```

2. This location will be used by Django to serve the image through the `MEDIA_URL` configuration.

## Step 2: Create Trending Products

Run the following Django management command in your terminal:

```bash
python manage.py add_trending_cpus
```

This command will:
- Create a "Processors" category if it doesn't exist
- Add trending CPU products (Intel i9-14900K, AMD Ryzen 9 7950X3D, etc.)
- Mark them as featured (is_featured=True) so they appear in the "Trending Hardware" section
- Associate them with your CPU image

## Step 3: Verify in Admin Panel

1. Go to http://localhost:8000/admin/products/product/
2. You should see the trending CPUs listed
3. They should have "is_featured" checked ✓

## Directory Structure After Setup

```
pcshop/
├── media/
│   └── products/
│       ├── trending_cpu_chip.png       ← Your CPU image
│       └── [other product images]
└── products/
    └── management/
        └── commands/
            └── add_trending_cpus.py    ← The command
```

## Adding More Trending Products

To add more trending hardware types (GPUs, RAM, Storage, etc.):

1. Edit the `add_trending_cpus.py` management command
2. Add more product definitions to the `cpus_data` list
3. Or create new management commands like `add_trending_gpus.py`

## Notes

- Products marked with `is_featured=True` appear in the home page "Trending Hardware" section
- Maximum 6 trending products are shown on the home page (controlled by `[:6]` in `products/views.py`)
- Images are stored in `media/products/` and served by Django's `MEDIA_URL`
