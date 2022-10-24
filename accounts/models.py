import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name"]
