from django.urls import path
from account_app.views import UserRegistrationAPIView, LoginAPIView, LogoutAPIView, ForgotPasswordApiView, VerifyVerificationCode
from account_app.views import  SetPasswordApiView, ProfileListAPIView, ProfileDetailAPIView, ProfileUpdateAPIView

urlpatterns = [
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('forgot_password/', ForgotPasswordApiView.as_view(),name='forgot_password'),
    path('verify_verification_code/', VerifyVerificationCode.as_view(), name='verify_verification_code'),
    path('reset_password/', SetPasswordApiView.as_view(), name='set_new_password'),
    path('profiles/', ProfileListAPIView.as_view(), name='profile-list'),
    path('profile/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    
]
