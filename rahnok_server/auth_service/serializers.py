from rest_framework import serializers


class TokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)