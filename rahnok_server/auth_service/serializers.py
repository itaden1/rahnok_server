from rest_framework import serializers


class VerifyTokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
