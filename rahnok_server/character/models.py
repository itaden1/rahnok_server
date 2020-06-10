import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField

from auth_service.models import User


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Character(BaseModel):

    DEFAULT_TRANSFORM = {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'o': 0.0
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=12, blank=False, null=False)
    last_name = models.CharField(max_length=12, blank=False, null=False)
    level = models.IntegerField(default=1)
    transform_x = JSONField(default=DEFAULT_TRANSFORM)
    transform_y = JSONField(default=DEFAULT_TRANSFORM)
    transform_z = JSONField(default=DEFAULT_TRANSFORM)
    transform_o = JSONField(default=DEFAULT_TRANSFORM)
    biome = models.IntegerField(default=1)
    appearance = JSONField(default=dict)

    
    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"
