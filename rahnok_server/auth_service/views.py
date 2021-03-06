from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_api_key.permissions import HasAPIKey

from auth_service.serializers import TokenRequestSerializer
from auth_service.authentication import GameServerAuthentication


#################################################
#           Web Client endpoints                #
#################################################

class AuthTokenLogin(ObtainAuthToken):

    """Obtain or create a login token using username / password
    Only accesable through the web application
    username / password should never be passed to the game server"""

    def post(self, request, *args, **kwargs):
        """ get or create a users authentication token"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        user_token, _ = Token.objects.get_or_create(
            user=user
        )

        return Response({"token": user_token.key}, status=status.HTTP_200_OK)

auth_token_login_view = AuthTokenLogin().as_view()


class DeleteUserAuthToken(APIView):
    """ Log th user out of the web application and delete the Auth token"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        user = request.user
        auth = request.auth

        auth.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

auth_logout_user_view = DeleteUserAuthToken.as_view()


#################################################
#           Game server endpoints               #
#################################################

class VerifyAuthToken(APIView):
    """Get user id from the Auth Token, This should only be accessed from the game server.
     it is used to make further queries on behalf of the player, for example updating their character"""
    # TODO fix api keys
    # permission_classes = [HasAPIKey]
    serializer_class = TokenRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = Token.objects.filter(key=serializer.validated_data.get("token")).first()
        if token:
            response = Response({
                "verified": True,
                "user_id": token.user.id, 
                "token": token.key
                }, status=status.HTTP_200_OK)
        else:
            response = Response({
                "verified": False,
                "token": serializer.validated_data.get("token")
                }, status=status.HTTP_410_GONE)
        return response

auth_token_verify_view = VerifyAuthToken().as_view()


class DeletePlayerAuthToken(APIView):
    """ Used by the game server when logging a player out. Deletes the Auth token """

    permission_classes = [HasAPIKey]
    serializer_class = TokenRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = Token.objects.get(key=serializer.validated_data.get("token"))
        token.delete()

        return Response({}, status=status.HTTP_200_OK)

auth_logout_player_view = DeletePlayerAuthToken().as_view()