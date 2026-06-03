from .views import get_or_create_cart

def cart_counter(request):
    try:
        cart = get_or_create_cart(request)
        return {'cart_item_count': cart.total_items}
    except Exception:
        return {'cart_item_count': 0}
