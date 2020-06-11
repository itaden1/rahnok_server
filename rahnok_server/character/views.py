from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from character.models import Character

from character.mixins import GetValidateUserMixin
from character.serializers import CharacterSerializer


class CharacterWebView(mixins.ListModelMixin, GenericAPIView):
    """used when a user wants to see characters on a website"""
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

character_web_view = CharacterWebView().as_view()


class CharacterListGameServerView(GetValidateUserMixin, GenericAPIView):
    """For retrieving and creating characters at character select screen"""
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

        # check user can create more characters
        if len(Character.objects.filter(user=user)) >= 3:
            return Response({"message": "max characters reached"})

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

character_list_game_server_view = CharacterListGameServerView().as_view()


class CharacterDetailGameServerView(GetValidateUserMixin, GenericAPIView):
    """For retrieving and updating or deleting single characters"""

    permission_classes = [HasAPIKey]
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    def get_queryset(self, user):
        return self.queryset.filter(user=user, pk=self.kwargs["uuid"])

    def get(self, request, *args, **kwargs):
        # check the token and get user
        user = self.get_validated_user(request)

        # get character via id in request data + user
        queryset = self.get_queryset(user).first()

        if queryset:
            serializer = self.get_serializer(queryset)
            # return the character data
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        # check the token and get user
        user = self.get_validated_user(request)

        queryset = self.get_queryset(user)

        if queryset:
            # get data from request
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # update the character with data
            queryset.update(**serializer.validated_data)
            updated_character = self.get_queryset(user).first()
            serializer = self.get_serializer(updated_character)
            # return success code
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        # check the token and get user
        user = self.get_validated_user(request)

        queryset = self.get_queryset(user)
        if queryset:
            character =queryset.first()
            character.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


character_detail_game_server_view = CharacterDetailGameServerView().as_view()
