from django.test import TestCase

from character.serializers import TransformSerializer, CharacterSerializer

# Create your tests here.
class TestCustomSerializerValidation(TestCase):
    
    def test_transform_serializer_good_data(self):
        good_data = {
                'x': 1.4,
                'y': 30.4,
                'z': 17.1,
            }

        serializer = TransformSerializer(data=good_data)
        self.assertTrue(serializer.is_valid())


    def test_character_validation_succeeds(self):
        data = {
            "first_name": "Malkar",
            "last_name": "Aurus",
            "level": 1,
            "transfrom_x": {'x': 0, 'y': 0, 'z': 0},
            "transfrom_y": {'x': 0, 'y': 0, 'z': 0},
            "transfrom_z": {'x': 0, 'y': 0, 'z': 0},
            "transfrom_o": {'x': 0, 'y': 0, 'z': 0},
            "appearance":{
                "body": 1,
                "beard": 0,
                "hair": 2,
            }
        }
        serializer = CharacterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
