from django.db import models
from User.models import User
import os
from django.urls import reverse
from django.conf import settings


# -*- coding: utf-8 -*-
# Create your models here.
class Student(User):
    student_code = models.CharField(max_length=20, unique=True, null=False, primary_key=True)

    def path_and_rename(self, name):
        filename = ''
        name, ext = os.path.split(self.student_video_data.name)
        # get filename
        if self.student_code:
            filename = 'students/{0}/videos/{1}_{2}'.format(self.student_code, self.student_code,
                                                            self.student_video_data.name)
        else:
            filename = 'students/{0}{1}'.format(name, self.student_video_data.name)
        # return the whole path to the file
        return filename

    student_video_data = models.FileField(upload_to=path_and_rename, blank=True, null=True)
    comment = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "" + self.first_name + self.last_name

    def get_student_code(self):
        return str(self.student_code)

    def get_absolute_url(self):
        return reverse('student:student_edit', kwargs={'student_code': self.student_code})

    def save(self, *args, **kwargs):
        # default username and password
        self.is_student = True
        self.is_staff = True
        if self.student_video_data is None:
            self.student_video_data = ""
        self.email = "" + self.get_student_code() + "@gm.uit.edu.vn"
        self.last_name = ""
        self.username = "" + str(self.student_code)
        # self.password = "" + str(self.student_code)
        self.set_password(str(self.student_code))
        super(Student, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quản lý học sinh'


class StudentImagesData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)

    # image_code = models.AutoField(primary_key=True)
    def path_and_rename(self, name):
        filename = ''
        name, ext = os.path.split(self.image_data.name)
        # get filename
        if self.student:
            filename = 'students/{0}/images/{1}_{2}'.format(self.student, self.student, self.image_data.name)
        else:
            filename = 'students/images/{0}{1}'.format(name, self.image_data.name)
        # return the whole path to the file
        return filename

    # save picture to student folder
    image_data = models.FileField(upload_to=path_and_rename, blank=False, null=False)
    image_date_upload = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        super(StudentImagesData, self).save(*args, **kwargs)

    def __str__(self):
        return self.image_data.name
