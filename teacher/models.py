from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from uuid import uuid4
from django.urls import reverse
# -*- coding: utf-8 -*-

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

# Create your models here.
class Teacher(User):
    # -*- coding: utf-8 -*-
    teacher_code = models.CharField(max_length=20, null=False, primary_key=True)
    teacher_image = models.ImageField(upload_to='teachers/images', null=True)

    def get_absolute_url(self):
        return reverse('teacher_edit', kwargs={'teacher_code': self.teacher_code})
