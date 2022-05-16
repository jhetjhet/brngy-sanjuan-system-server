from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class BrngyUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)