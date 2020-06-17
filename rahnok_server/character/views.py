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
        user, token = self.get_validated_user(request)
        characters = Character.objects.filter(user=user)

        serializer = self.get_serializer(characters, many=True)
        return Response({"token": token, "character_data": serializer.data})
    
    def post(self, request, *args, **kwargs):
        # get user via token
        user, token = self.get_validated_user(request)

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
        return Response({token: serializer.data}, status=status.HTTP_201_CREATED)



character_list_game_server_view = CharacterListGameServerView().as_view()


class BulkUpdateCharacterView(GenericAPIView):
    """Perform a bulk update on all connected players"""
    permission_classes = [HasAPIKey]
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get("players"), many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        id_list = [i["id"] for i in data]
        objects = self.get_queryset().filter(id__in=id_list).all()

        try:
            # update all objects
            for ob in objects:
                for d in data:
                    if d["id"] == ob.id:
                        ob.transform_x = d["transform_x"]
                        ob.transform_y = d["transform_y"]
                        ob.transform_z = d["transform_z"]
                        ob.transform_o = d["transform_o"]
            Character.objects.bulk_update(
                objects, 
                fields=["transform_x", "transform_y", "transform_z", "transform_o"],
                batch_size=100
                )
            
            serializer = self.get_serializer(self.get_queryset().filter(id__in=id_list), many=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            # TODO log errors somewhere
            return Response(status=status.HTTP_400_BAD_REQUEST)

bulk_update_character_view = BulkUpdateCharacterView().as_view()


class CharacterDetailGameServerView(GetValidateUserMixin, GenericAPIView):
    """For retrieving and updating or deleting single characters"""

    permission_classes = [HasAPIKey]
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs["uuid"])

    def get(self, request, *args, **kwargs):
        # check the token and get user
        user, token = self.get_validated_user(request)

        queryset = self.get_queryset().filter(user_id=user.id).first()

        if queryset:
            serializer = self.get_serializer(queryset)
            # return the character data
            return Response({"token": token, "character_data": serializer.data}, status=status.HTTP_200_OK)
        return Response(status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        # check the token and get user
        user, _ = self.get_validated_user(request)

        queryset = self.get_queryset().filter(user_id=user.id).first()

        if queryset:
            # get data from request
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # update the character with data
            queryset.update(**serializer.validated_data)
            updated_character = self.get_queryset().filter(user_id=user.id).first()
            serializer = self.get_serializer(updated_character)
            # return success code
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        # check the token and get user
        user, _ = self.get_validated_user(request)

        queryset = self.get_queryset().filter(user_id=user.id)
        if queryset:
            character = queryset.first()
            character.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


character_detail_game_server_view = CharacterDetailGameServerView().as_view()
