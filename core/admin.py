from django.contrib import admin
from .models import OrderItem, Order, Item, CategoryItem

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

# Register your models here.

admin.site.register(OrderItem)
# admin.site.register(Item)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(CategoryItem)