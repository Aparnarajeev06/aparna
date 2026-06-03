from django.contrib import admin
from .models import PCBuild

@admin.register(PCBuild)
class PCBuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'cpu', 'gpu', 'total_price', 'is_compatible', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'total_price', 'total_wattage', 'is_compatible')
    
    fieldsets = (
        ('Build Information', {
            'fields': ('user', 'name')
        }),
        ('PC Components', {
            'fields': ('cpu', 'motherboard', 'ram', 'gpu', 'storage', 'psu')
        }),
        ('Build Statistics', {
            'fields': ('total_price', 'total_wattage', 'is_compatible'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
