import uuid

from django.db import models

from auth_service.models import User


class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=12, blank=False, null=False)
    last_name = models.CharField(max_length=12, blank=False, null=False)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"
