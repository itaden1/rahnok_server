
from auth_service.serializers import TokenRequestSerializer
from rest_framework.authtoken.models import Token


class GetValidateUserMixin:

    def get_validated_user(self, request):
        serializer = TokenRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = Token.objects.filter(key=serializer.validated_data.get("token")).first().user
        return user