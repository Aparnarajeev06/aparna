from django.contrib import admin
from .models import FAQ, Ticket, TicketReply, RMARequest

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    list_filter = ('category',)
    search_fields = ('question', 'answer')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('subject', 'user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('subject', 'user', 'category', 'status')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0
    readonly_fields = ('sender', 'created_at', 'message')
    can_delete = False
    fields = ('sender', 'message', 'created_at')

@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'created_at')
    list_filter = ('created_at', 'sender')
    search_fields = ('ticket__subject', 'sender__username', 'message')
    readonly_fields = ('created_at',)

@admin.register(RMARequest)
class RMARequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'order_item__product__name', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('RMA Information', {
            'fields': ('user', 'order_item', 'status')
        }),
        ('Request Details', {
            'fields': ('reason',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def product_name(self, obj):
        return obj.order_item.product.name if obj.order_item.product else 'Unknown Part'
    product_name.short_description = 'Product'
