from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
import re

User = get_user_model()


class UserValidationMixin:
    def validate_email(self, value):
            if not value:
                raise serializers.ValidationError("Email is required.")
            try:
                validate_email(value)
            except ValidationError:
                raise serializers.ValidationError("Invalid email format.")
            
            if not re.search(r'@afexnigeria\.com$', value):
                raise serializers.ValidationError("Email must be from @afexnigeria.com domain.")
            return value
        

    def validate_password(self, value):

            if not value:
                raise serializers.ValidationError("Password is required.")
            try:
                validate_password(value)
            except ValidationError:
                raise serializers.ValidationError("Invalid password format, password must contain an upper case letter, a lower case letter, a digit and special character.")
            return value


    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required.")

        african_number_pattern = re.compile(r'^\+?(?:[0-9]\s?){6,14}[0-9]$')
        if not african_number_pattern.match(value):
            raise ValidationError("Phone number must be in a valid African format.")


    def validate_state_code(self, value):
        if not value:
            raise serializers.ValidationError("You have to enter your state code.")
        if len(value) != 2:
            raise serializers.ValidationError("Invalid state code, your state code is the two letters representing the state you are")
        return value
