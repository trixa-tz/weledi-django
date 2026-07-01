from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model based on Django's AbstractUser.

    Using an abstract base now means we can add fields later without a
    painful migration. Login still happens with `username` + `password`.
    """

    phone = models.CharField(max_length=30, blank=True)
    is_auditor = models.BooleanField(
        default=False,
        help_text="Auditors can review system activity.",
    )

    def __str__(self):
        return self.username
