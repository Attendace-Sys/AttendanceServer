from django.db import models
#(01-delete) from teacher.models import User
import os

# Create your models here.
class Student(models.Model):
    
    student_code = models.CharField(max_length=20, unique=True, null=False, primary_key=True)
    # lock user and change to manual field#(01-add)
    #(01-delete) user = models.ManyToManyField(User, related_name="student_user")
    full_name = models.CharField(max_length=50, unique=True, null=False) #(01-add)
    email = models.EmailField(max_length=50, blank=False, null=False)#(01-add)
    # end change#(01-add)
    def path_and_rename(self, name):
        filename=''
        name, ext = os.path.split(self.student_video_data.name)
        # get filename
        if self.student_code:
            filename = 'students/{0}/videos/{1}_{2}'.format(self.student_code, self.student_code, self.student_video_data.name)
        else:
            filename = 'students/{0}{1}'.format(name, self.student_video_data.name)
        # return the whole path to the file
        return filename
    student_video_data = models.FileField(upload_to=path_and_rename, blank=False, null=True)
    def __str__(self):
        return self.student_code

    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)

class StudentImagesData(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    def path_and_rename(self, name):
        filename=''
        name, ext = os.path.split(self.image_data.name)
        # get filename
        if self.student:
            filename = 'students/{0}/images/{1}_{2}'.format(self.student, self.student, self.image_data.name)
        else:
            filename = 'students/images/{0}{1}'.format( name, self.image_data.name)
        # return the whole path to the file
        return filename
    # save picture to student folder
    image_data = models.FileField(upload_to=path_and_rename, blank=False, null=True)
    image_date_upload = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        super(StudentImagesData, self).save(*args, **kwargs)
    