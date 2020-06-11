from rest_framework import serializers



class TransformSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    z = serializers.FloatField()


class CharacterSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    level = serializers.IntegerField(required=False)
    transform_x = TransformSerializer()
    transform_y = TransformSerializer()
    transform_z = TransformSerializer()
    transform_o = TransformSerializer()
    appearance = serializers.JSONField()

    def validate_appearance(self, appearance):
        if appearance is None:
            raise serializers.ValidationError("appearance field is required")
        if appearance["body"] not in [1,2]:
            raise serializers.ValidationError("unknown body model reference")
        if appearance["beard"] not in [0,1]:
            raise serializers.ValidationError("unknown beard model reference")
        if appearance["hair"] not in [0,1,2]:
            raise serializers.ValidationError("unknown hair model reference")

        return appearance