from django.db import models
from django.contrib.auth.models import AbstractUser
from User.models import User
from guardian.shortcuts import assign_perm
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
        permissions = (
        )

    def __str__(self):
        return self.first_name + self.last_name

    def save(self, *args, **kwargs):
        # default username and password
        self.is_teacher = True
        self.is_staff = True
        self.last_name = ""
        if self.username == "":
            self.username = "" + self.teacher_code
        if self.password == "":
            self.password = "" + self.teacher_code
        self.set_password(self.password)
        super(Teacher, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Teacher, self).__init__(*args, **kwargs)
