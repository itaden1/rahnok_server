from rest_framework import serializers





class TransformSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    z = serializers.FloatField()


class CharacterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    level = serializers.IntegerField()
    transfrom_x = TransformSerializer()
    transfrom_y = TransformSerializer()
    transfrom_z = TransformSerializer()
    transfrom_o = TransformSerializer()
    appearance = serializers.JSONField()

    def validate_appearance(self, appearance):
        if appearance["body"] not in [1,2]:
            raise serializers.ValidationError("unknown body model reference")
        if appearance["beard"] not in [0,1]:
            raise serializers.ValidationError("unknown beard model reference")
        if appearance["hair"] not in [0,1,2]:
            raise serializers.ValidationError("unknown beard model reference")

