from django.db import models
from student.models import Student
from teacher.models import Teacher

# Create your models here.

class Course(models.Model):
    course_code = models.CharField(max_length=20, null=False)
    course_name = models.CharField(default='Course name', max_length=50, null=False)
    start_day = models.DateTimeField(null=True)
    end_day = models.DateTimeField(null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

class StudentsInCourseDetail(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False,)

class CourseScheduleDetail(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)

class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    schedule_code = models.CharField(max_length=20, null=False)
    schedule_date = models.DateTimeField(auto_now_add=True, null=False)
    schedule_numberof_day = models.IntegerField(null=False)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    schedule_code = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=False)
    absent_status = models.BooleanField(default=False)
    # save to student_name folder
    image_data = models.FileField(upload_to='media/students/images/{student_code(student_name)}', blank=False, null=False)