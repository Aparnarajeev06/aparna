from django.contrib import admin
from .models import Profile, Address

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_profile')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('user',)
    readonly_fields = ('user',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone',)
        }),
        ('Profile Details', {
            'fields': ('avatar', 'bio')
        }),
    )
    
    def created_profile(self, obj):
        return obj.user.date_joined
    created_profile.short_description = "Account Created"

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'postal_code', 'is_default')
    list_filter = ('country', 'is_default', 'user')
    search_fields = ('user__username', 'street', 'city', 'postal_code')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Address Details', {
            'fields': ('street', 'city', 'state', 'postal_code', 'country')
        }),
        ('Default Address', {
            'fields': ('is_default',)
        }),
    )
