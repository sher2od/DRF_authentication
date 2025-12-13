from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = [
        ['ADMIN','Admin'],
        ['USER','User'],
        ['MANAGER','Manager']
    ]

    role = models.CharField(
        choices=ROLES,
        default='USER'
    )

    @property
    def is_admin(self):
        return self.role == "ADMIN"
    
    @property
    def is_user(self):
        return self.role == "USER"
    
    @property
    def is_manager(self):
        return self.role == "MANAGER"