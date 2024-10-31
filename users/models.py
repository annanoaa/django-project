from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    last_active_datetime = models.DateTimeField(null=True, blank=True)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'custom_user'