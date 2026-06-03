from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('total_price',)
    fields = ('product', 'price', 'quantity', 'total_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'user', 'total_price', 'shipping_status', 'payment_status', 'created_at')
    list_filter = ('shipping_status', 'payment_status', 'created_at')
    search_fields = ('tracking_number', 'user__username', 'email', 'phone')
    readonly_fields = ('tracking_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('tracking_number', 'user')
        }),
        ('Customer Information', {
            'fields': ('email', 'phone')
        }),
        ('Shipping & Address', {
            'fields': ('shipping_address',)
        }),
        ('Status & Payment', {
            'fields': ('shipping_status', 'payment_status', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'total_price')
    list_filter = ('order__created_at', 'product__category')
    search_fields = ('order__tracking_number', 'product__name')
    readonly_fields = ('total_price',)
