from rest_framework import serializers


class TransformSerializer(serializers.Serializer):
    transform = serializers.JSONField()

class CharacterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    transfrom = TransformSerializer()

