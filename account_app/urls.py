from django.urls import path
from account_app.views import UserRegistrationAPIView, LoginAPIView, LogoutAPIView
from account_app.views import ProfileListAPIView, ProfileDetailAPIView, ProfileUpdateAPIView

urlpatterns = [
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profiles/', ProfileListAPIView.as_view(), name='profile-list'),
    path('profile/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    
]
