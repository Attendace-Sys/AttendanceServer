from django.db import models
from User.models import User
import os
from keras.preprocessing.image import load_img, save_img, img_to_array
from django.urls import reverse
from django.conf import settings
import numpy as np
import face_recognition
from keras.preprocessing.image import load_img
import random


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
        return "" + self.student_code

    def get_student_code(self):
        return str(self.student_code)

    def get_absolute_url(self):
        return reverse('student:student_edit', kwargs={'student_code': self.student_code})

    def save(self, *args, **kwargs):
        # default username and password
        self.is_student = True
        self.is_staff = True
        if self.email == "":
            self.email = "" + self.get_student_code() + "@gm.uit.edu.vn"
        self.last_name = ""
        if self.username == "":
            self.username = "" + str(self.student_code)
        if self.password == "":
            self.password = "" + str(self.student_code)
        self.set_password(self.password)
        super(Student, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quản lý học sinh'


def preprocess_image(image_path):
    img = load_img(image_path, target_size=(160, 160))
    return np.array(img)


class StudentImagesData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)

    # image_code = models.AutoField(primary_key=True)
    def path_and_rename(self, name):
        filename = ''
        name, ext = os.path.split(self.image_data.name)
        # get filename
        if self.student:
            filename = 'students/{0}/images/{1}'.format(self.student, self.image_data.name)
        else:
            filename = 'students/images/{0}{1}'.format(name, self.image_data.name)
        # return the whole path to the file
        return filename

    # save picture to student folder
    image_data = models.FileField(upload_to=path_and_rename, blank=False, null=False)
    image_date_upload = models.DateTimeField(auto_now_add=True, null=True)

    def convert_image_to_text(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        npy = ".npy"
        STUDENT_IMG_DIR = BASE_DIR + '/media/'
        filename = STUDENT_IMG_DIR + self.image_data.name
        filepath, ext = os.path.splitext(filename)
        if os.path.isfile(filepath + npy) is False:
            if os.path.isfile(filename) is False:
                img = preprocess_image(filename)
            try:
                img_vector = face_recognition.face_encodings(img, known_face_locations=[(0, 160, 160, 0)])[0]
                np.save(filepath, img_vector)
            except:
                pass

    def save(self, *args, **kwargs):
        super(StudentImagesData, self).save(*args, **kwargs)
        self.convert_image_to_text(self, *args, **kwargs)

    def __str__(self):
        return self.image_data.name
