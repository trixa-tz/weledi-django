import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model based on Django's AbstractUser.

    Using an abstract base now means we can add fields later without a
    painful migration. Login still happens with `username` + `password`.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=30, blank=True)
    is_editor = models.BooleanField(
        default = False,
        help_text = "Editors can publish news to the public.",
    )

    def __str__(self):
        return self.username
