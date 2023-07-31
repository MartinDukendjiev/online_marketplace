from django.contrib import admin
from .models import Product, Category # SubCategory


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'user', 'upload_date', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description', 'price', 'category__name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
# admin.site.register(SubCategory)
