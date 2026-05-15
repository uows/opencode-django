from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Alumno'
        TEACHER = 'TEACHER', 'Profesor'
        ADMIN = 'ADMIN', 'Administrador'

    username = None
    email = models.EmailField('email', unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'
