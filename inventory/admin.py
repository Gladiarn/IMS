from django.contrib import admin
from .models import Product, Category, Supplier, Order, Customer, CustomUser

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock_quantity', 'created_by', 'created_at')
    list_filter = ('created_at', 'category', 'supplier')
    search_fields = ('name', 'sku', 'description')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer','product', 'order_date', 'total_price')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'phone', 'email')
    search_fields = ('name', 'contact_name')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'usertype')
    search_fields = ('username', 'usertype')



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Supplier, SupplierAdmin)
