import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField

from auth_service.models import User


def get_default_appearance():
        return {
        "body": 1,
        "hair": 0,
        "beard": 0
    }

def get_default_transform():
    return {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'o': 0.0
    }

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Character(BaseModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=12, blank=False, null=False)
    last_name = models.CharField(max_length=12, blank=False, null=False)
    level = models.IntegerField(default=1)
    transform_x = JSONField(default=get_default_transform)
    transform_y = JSONField(default=get_default_transform)
    transform_z = JSONField(default=get_default_transform)
    transform_o = JSONField(default=get_default_transform)
    biome = models.IntegerField(default=1)
    appearance = JSONField(default=get_default_appearance)

    class Meta:
        unique_together = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"
