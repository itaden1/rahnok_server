from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from character.models import Character

from character.serializers import CharacterSerializer
from auth_service.serializers import TokenRequestSerializer
from rest_framework.authtoken.models import Token


class CharacterWebView(mixins.ListModelMixin, GenericAPIView):

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

character_web_view = CharacterWebView().as_view()


class CharacterGameServerView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = CharacterSerializer


    def get(self, request, *args, **kwargs):
        serializer = TokenRequestSerializer(data=request.data)
        serializer.is_valid(raise_exeption=True)
        user = Token.objects.filter(key=serializer.validated_data.get("token")).first().user
        characters = Character.objects.filter(user=user)

        response_serializer = self.get_serializer(characters, many=True)
        return Response(response_serializer)

    def retrieve(self, request, *args, **kwargs):
        # check the token

        # get user via the token

        # get character via id in request data + user

        # return the character data
        pass

    def update(self, request, *args, **kwargs):
        pass
        # check the token

        # get user via the token

        # get character via id in request data + user

        # get data from request

        # update the character with data

        # return success code

    def create(self, request, *args, **kwargs):
        pass
        # check the token

        # get user via token

        # get character data from request

        # create a new character for the user

        # return success code

character_game_server_view = CharacterGameServerView().as_view()