from django.db import models

# Create your models here.
import os
from uuid import uuid4
from django.urls import reverse
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    username = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Username must be alphanumberic or contain number',
                           code='invalid_username'
                           )
        ],
        unique=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name_plural = 'Quản lý account'

