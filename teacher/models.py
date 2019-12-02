from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from uuid import uuid4

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    teacher_code = models.CharField(max_length=20, null=False, primary_key=True)
    teacher_email = models.EmailField(max_length=50, null=True, unique=True)
    # 1 teacher have 1 image no need to split more
    teacher_image = models.ImageField(upload_to='teachers/images', null=True)
    teacher_name = models.CharField(max_length=20, null=False)
    