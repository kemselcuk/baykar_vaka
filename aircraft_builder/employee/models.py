from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from teams.models import Team

class Employee(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='employee_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_permissions',
        blank=True,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='employees'
    )

    def __str__(self):
        return self.username