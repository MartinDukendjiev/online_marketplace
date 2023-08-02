from django.urls import path
from .views import IndexView, about_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', about_view, name='about'),
]