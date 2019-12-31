from django.db import models
from guardian.shortcuts import assign_perm
from django.utils.translation import gettext_lazy as _
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
    # label = 'Student Name'
    first_name = models.CharField(_('Full name'), max_length=30, blank=True)
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
        if self.is_superuser:
            return True
        if self.is_teacher:
            if perm == 'student.add_student' or perm == 'student.change_student' or \
                    perm == 'student.delete_student' or perm == 'student.view_student' or \
                    perm == 'student.add_studentimagesdata' or perm == 'student.change_studentimagesdata' or \
                    perm == 'student.delete_studentimagesdata' or perm == 'student.view_studentimagesdata' or \
                    perm == 'course.add_course' or perm == 'course.change_course' or \
                    perm == 'course.delete_course' or perm == 'course.view_course' or \
                    perm == 'course.add_schedule' or perm == 'course.change_schedule' or \
                    perm == 'course.delete_schedule' or perm == 'course.view_schedule' or \
                    perm == 'course.add_scheduleimagesdata' or perm == 'course.change_scheduleimagesdata' or \
                    perm == 'course.delete_scheduleimagesdata' or perm == 'course.view_scheduleimagesdata' or \
                    perm == 'course.add_attendance' or perm == 'course.change_attendance' or \
                    perm == 'course.delete_attendance' or perm == 'course.view_attendance' or \
                    perm == 'User.add_user' or perm == 'User.change_user' or \
                    perm == 'User.view_user' or \
                    perm == 'teacher.change_teacher' or \
                    perm == 'teacher.view_teacher':
                return True
        if self.is_student:
            if perm == 'student.change_student' or perm == 'student.view_student' or \
                    perm == 'course.add_course' or perm == 'course.change_course' or \
                    perm == 'course.view_course' or perm == 'course.view_schedule' or \
                    perm == 'course.view_scheduleimagesdata' or perm == 'course.view_attendance':
                return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name_plural = 'Quản lý account'
