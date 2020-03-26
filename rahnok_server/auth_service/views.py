from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


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
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        
        user = request.user
        auth = request.auth

        auth.delete()
        return Response({"res": auth.key})

auth_token_logout_view = AuthTokenLogout.as_view()

