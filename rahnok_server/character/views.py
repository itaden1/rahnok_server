from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from character.models import Character

from character.mixins import GetValidateUserMixin
from character.serializers import CharacterSerializer


class CharacterWebView(mixins.ListModelMixin, GenericAPIView):

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

character_web_view = CharacterWebView().as_view()


class CharacterListGameServerView(GetValidateUserMixin, GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = CharacterSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_validated_user(request)
        characters = Character.objects.filter(user=user)

        serializer = self.get_serializer(characters, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        # get user via token
        user = self.get_validated_user(request)

        # get character data from request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create a new character for the user
        data = serializer.validated_data

        new_character = Character.objects.create(
            user=user,
            first_name=data["first_name"],
            last_name=data["last_name"],
            appearance=data["appearance"],
            transform_x=data["transform_x"],
            transform_y=data["transform_y"],
            transform_z=data["transform_z"],
            transform_o=data["transform_o"],
            )

        serializer = self.get_serializer(new_character)        
        
        # return success code
        return Response(serializer.data)

character_list_game_server_view = CharacterListGameServerView().as_view()


class CharacterDetailGameServerView(GetValidateUserMixin, GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = CharacterSerializer

    def get_queryset(self, user):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return super().get_queryset().filter(id=lookup_url_kwarg, user=user)

    def get(self, request, *args, **kwargs):
        # check the token and get user
        user = self.get_validated_user(request)

        # get character via id in request data + user
        queryset = self.get_queryset(user)

        serializer = self.get_serializer(queryset)
        # return the character data
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pass
        # check the token

        # get user via the token

        # get character via id in request data + user

        # get data from request

        # update the character with data

        # return success code

    def delete(self, request, *args, **kwargs):
        pass
        # check token and get user

        # get queryset

        # delete character

character_detail_game_server_view = CharacterDetailGameServerView().as_view()
