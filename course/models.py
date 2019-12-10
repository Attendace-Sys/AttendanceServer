from django.db import models
from student.models import Student
from teacher.models import Teacher


# Create your models here.

class Course(models.Model):
    course_code = models.CharField(max_length=20, null=False, primary_key=True)
    course_name = models.CharField(default='Course name', max_length=50, null=False)
    start_day = models.DateTimeField(null=True)
    end_day = models.DateTimeField(null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student)

    class Meta:
        verbose_name_plural = 'Courses List'


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    schedule_code = models.CharField(max_length=20, null=False, primary_key=True)
    schedule_date = models.DateTimeField(auto_now_add=True, null=False)
    schedule_number_of_day = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = 'Schedule'


class Attendance(models.Model):
    attendance_code = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    schedule_code = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=False)
    absent_status = models.BooleanField(default=False)
    # save to student_name folder
    image_data = models.FileField(upload_to='media/students/images/}', blank=False, null=False)
