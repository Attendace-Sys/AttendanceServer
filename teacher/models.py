from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from uuid import uuid4
from django.urls import reverse
from django.utils import timezone


# -*- coding: utf-8 -*-

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


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
        self.last_name = ""
        self.username = "" + self.teacher_code
        self.password = "" + self.teacher_code
        super(Teacher, self).save(*args, **kwargs)