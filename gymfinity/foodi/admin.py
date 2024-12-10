from django.contrib import admin
from .models import food, discount, CartItem, UserProfile, Order

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Display phone number in list view
    search_fields = ('user__username', 'phone_number')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at', 'phone_number')
    search_fields = ('user__username', 'user__email', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    filter_horizontal = ('items',)  # To easily manage ManyToMany relationships in the admin

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'quantity')

# Registering models and custom admin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(food)
admin.site.register(discount)
