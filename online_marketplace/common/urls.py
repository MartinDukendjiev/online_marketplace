from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import IndexView, about_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', about_view, name='about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
