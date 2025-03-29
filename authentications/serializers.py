from django.contrib.auth import authenticate
from rest_framework import serializers
from authentications.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password
        password = validated_data.pop('password')  # Extract password

        user = User(**validated_data)  # Create user instance without saving
        user.set_password(password)  # Hash and set password
        user.save()  # Save user to database

        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_active:
            raise serializers.ValidationError('User is inactive.')

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        
