from django.db import models
from teacher.models import User
import os

# Create your models here.
class Student(User):
    user = models.ManyToManyField(User, related_name="student_user")
    student_code = models.CharField(max_length=20, unique=True, null=False, primary_key=True)
    # student_name = models.CharField(max_length=20, null=False)
    # student_email = models.EmailField(default='student@email.com', max_length=50, null=True, unique=True)
    # video is only use to setting for first time detection
    student_video_data = models.FileField(upload_to='students/video', blank=False, null=True)
    def __str__(self):
        return self.student_code

class StudentImagesData(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    # image_name = models.CharField(max_length=20, null=True, )
    def path_and_rename(self, name):
        filename=''
        name, ext = os.path.split(self.image_data.name)
        # get filename
        if self.student:
            filename = 'student/{0}_{1}'.format(self.student, self.image_data.name)
        else:
            filename = 'student/{0}.{1}'.format( name, self.image_data.name)
        # return the whole path to the file
        return filename
    # save picture to student folder
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_data = models.FileField(upload_to=path_and_rename, blank=False, null=True)
    image_date_upload = models.DateTimeField(auto_now_add=True, null=True)
    