from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer,  EmailResetPasswordSerializer, ResetPasswordSerializer 
from .serializers import ProfileSerializer, ProfileUpdateSerializer 
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import  AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser
from .tasks import send_email_fun
import random
import string
#import base64


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            'status': 'success',
            'password': serializer.instance.password,
            'email': serializer.instance.email,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            data = serializer.validated_data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)
            except Exception:
                return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordApiView(APIView):
    serializer_class = EmailResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if CustomUser.active_objects.filter(email__exact=email).exists():
                user = CustomUser.active_objects.get(email=email)
                
                # Generate a 6-character verification code
                verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                print(verification_code)
                user.verification_code =verification_code
                
                # Send the verification code to the user's email
                mail_subject = "Password Reset Verification Code"
                message = f"Hi {user.firstname},\n\n" \
                          f"Please use the following verification code to reset your password: {verification_code}"
                send_email_fun(subject=mail_subject, message = message, sender='otutaiwo1@gmail.com', receiver=user.email)
                return Response({"status": "success", "message": "We have sent a password-reset verification code to the email you provided. Please check and reset  "},status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": "The email provided doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class VerifyVerificationCode(APIView):

    def post(self, request, *args, **kwargs):
        verification_code = request.data.get('verification_code')
        try:
            user = CustomUser.active_objects.get(verification_code=verification_code)
        except CustomUser.DoesNotExist:
            return Response({"status": "fail", "message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
        # Reset the verification code after successful verification
        user.verification_code = ''
        user.save()
        return Response({"status": "success", "message": "Verification code is valid"}, status=status.HTTP_200_OK)



class SetPasswordApiView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        user = CustomUser.active_sobjects.get(email=email)
        user.set_password(new_password)
        user.save()   
        return Response({"status": "success", "message": "Password set successfully"}, status=status.HTTP_200_OK)



class ProfileListAPIView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return CustomUser.active_objects.all()


class ProfileDetailAPIView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.active_objects.all()
        else:
            return CustomUser.active_objects.filter(pk=self.request.user.pk)


class ProfileUpdateAPIView(UpdateAPIView):
    queryset = CustomUser.active_objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user