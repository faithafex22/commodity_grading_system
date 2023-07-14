from rest_framework import serializers
from .mixins import UserValidationMixin
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # confirm_password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField()
    state_code = serializers.CharField()
    user_picture = serializers.ImageField()

    def validate(self, data):
            password = data['password']
            confirm_password = self.context['request'].data['confirm_password']
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match")
            return data


    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name',  'state_code', 'phone_number', 'date_joined', 'user_picture']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is inactive.")

                refresh = RefreshToken.for_user(user)

                data['access_token'] = str(refresh.access_token)
                data['refresh_token'] = str(refresh)

                return data
            else:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Email and password are required.")

    def to_representation(self, instance):
        return {
            'access_token': instance['access_token'],
            'refresh_token': instance['refresh_token'],
            'message': 'User login successful.'
        }


class ProfileSerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField()
    user_picture = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'userid', 'phone_number', 'date_joined', 'user_picture']
        read_only_fields = ['email', 'user_id', 'date_joined']

    def get_userid(self, obj):
        return obj.generate_user_id()



class ProfileUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField(source='user.email')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = CustomUser
        fields = ['email', 'user_id', 'first_name', 'last_name', 'phone_number', 'user_picture', 'date_joined']
        read_only_fields = ['user_id', 'date_joined', 'email', 'first_name', 'last_name']



class EmailResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate_email(self, value):
        lower_email = value.lower()
        return lower_email
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

