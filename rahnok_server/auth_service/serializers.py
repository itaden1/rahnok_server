from rest_framework import serializers


class VerifyTokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class DeleteTokenRequestSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
