from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product list'),
    path('create/', ProductCreateView.as_view(), name='product create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product delete'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
