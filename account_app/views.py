from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import  AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser


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
    queryset = CustomUser.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user