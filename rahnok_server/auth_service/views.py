from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_api_key.permissions import HasAPIKey

from auth_service.serializers import VerifyTokenRequestSerializer
from auth_service.authentication import GameServerAuthentication


class AuthTokenLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """ get or create a users authentication token"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        user_token, _ = Token.objects.get_or_create(
            user=user
        )

        return Response({
            "user_id": user.id,
            "token": user_token.key
        })

auth_token_login_view = AuthTokenLogin().as_view()


class AuthTokenLogout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [HasAPIKey|IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        auth = request.auth

        auth.delete()
        return Response({"res": auth.key})

auth_token_logout_view = AuthTokenLogout.as_view()


class VerifyAuthToken(APIView):
    """Get user id from the Auth Token, This should only be accessed from the game server.
     it is used to make further queries on behalf of the player, for example updating their character"""

    #authentication_classes = (TokenAuthentication,)
    permission_classes = [HasAPIKey]
    print(permission_classes)
    request_serializer_class = VerifyTokenRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.request_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = Token.objects.get(key=serializer.validated_data.get("token")).user.id

        return Response({"user_id": user_id})

auth_token_verify_view = VerifyAuthToken().as_view()
