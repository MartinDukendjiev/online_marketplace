from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_marketplace.common.urls')),
    path('accounts/', include('online_marketplace.accounts.urls')),
    path('products/', include('online_marketplace.products.urls')),
]
