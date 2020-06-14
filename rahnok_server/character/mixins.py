
from auth_service.serializers import TokenRequestSerializer
from rest_framework.authtoken.models import Token


class GetValidateUserMixin:

    def get_validated_user(self, request):
        serializer = TokenRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get("token")
        user = Token.objects.filter(key=token).first().user
        return user, token