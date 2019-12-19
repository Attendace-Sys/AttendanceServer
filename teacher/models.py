from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from uuid import uuid4
from django.urls import reverse
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
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
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name_plural = 'Quản lý account'


# -*- coding: utf-8 -*-


# Create your models here.
class Teacher(User):
    teacher_code = models.CharField(max_length=20, null=False, primary_key=True)
    teacher_image = models.ImageField(upload_to='teachers/images', null=True)

    def get_absolute_url(self):
        return reverse('teacher:teacher_edit', kwargs={'teacher_code': self.teacher_code})

    """
    #we can add @property or get query set to create property column
    @property
    def days_since_creation(self):
        diff = timezone.now() - self.date_joined 
        return  (diff.days + 1).__str__() + ' Day since creation'
        """

    class Meta:
        verbose_name_plural = 'Quản lý giáo viên'

    def __str__(self):
        return self.first_name + self.last_name

    def save(self, *args, **kwargs):
        # default username and password
        self.is_teacher = True
        self.is_staff = True
        self.last_name = ""
        if self.username == "":
            self.username = "" + self.teacher_code
        print(self.username)
        if self.password == "":
            self.password = "" + self.teacher_code
        self.set_password(self.password)
        super(Teacher, self).save(*args, **kwargs)
