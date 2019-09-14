from rest_framework import serializers
# from rest_auth.serializers import UserDetailsSerializer
from .models import User


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "birthday")
