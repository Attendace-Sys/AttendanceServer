from django.db import models
#(01-delete)from django.contrib.auth.models import AbstractUser
import os
from uuid import uuid4
"""
# (01-delete)
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
"""

# Create your models here.
class Teacher(models.Model):
    teacher_code = models.CharField(max_length=20, null=False, primary_key=True)
    full_name = models.CharField(max_length=20, null=False) #(01-add)
    #(01-delete) user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)#(01-add)
    # 1 teacher have 1 image no need to split more
    teacher_image = models.ImageField(upload_to='teachers/images', null=True)
    
    