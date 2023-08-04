from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views
from .views import ProfileDetailView, UserRegisterView, UserLoginView, UserLogoutView, ProfileEditView, \
    ProfileDeleteView, add_rating

urlpatterns = [
    # localhost:8000/accounts/
    path('register/', UserRegisterView.as_view(), name="register user"),
    path('login/', UserLoginView.as_view(), name="login user"),
    path('logout/', UserLogoutView.as_view(), name="logout user"),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailView.as_view(), name='profile details'),
        path('edit/', ProfileEditView.as_view(), name='profile edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile delete'),
    ]))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
