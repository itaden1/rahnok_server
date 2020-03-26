import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token

# TODO fihure out why Token table is not saving user is as UUID
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
