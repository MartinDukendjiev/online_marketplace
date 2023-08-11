from django.contrib import admin
from .models import Product, Category, ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description', 'price', 'user', 'upload_date', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description', 'price', 'category__name',)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_filter = ('product',)
    search_fields = ('product',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
