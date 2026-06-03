from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('product', 'quantity', 'total_price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_or_guest', 'total_items', 'total_price', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created_at', 'updated_at', 'total_items', 'total_price')
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Cart Information', {
            'fields': ('user', 'session_key')
        }),
        ('Statistics', {
            'fields': ('total_items', 'total_price'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_or_guest(self, obj):
        return obj.user.username if obj.user else f"Guest ({obj.session_key[:8]}...)"
    user_or_guest.short_description = 'User/Session'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price', 'created_at')
    list_filter = ('created_at', 'product__category')
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ('created_at', 'total_price')
