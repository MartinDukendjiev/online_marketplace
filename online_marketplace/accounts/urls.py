from django.urls import path, include
from .views import ProfileDetailView, UserRegisterView, UserLoginView, UserLogoutView, ProfileEditView, \
    ProfileDeleteView

urlpatterns = [
    # localhost:8000/accounts/
    path('register/', UserRegisterView.as_view(), name="register user"),
    path('login/', UserLoginView.as_view(), name="login user"),
    path('logout/', UserLogoutView.as_view(), name="logout user"),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailView.as_view(), name='profile details'),
        path('edit/', ProfileEditView.as_view(), name='profile edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile delete')
    ]))
]
