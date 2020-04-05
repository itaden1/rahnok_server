from rest_framework import serializers


class TokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

