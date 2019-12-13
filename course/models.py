from django.db import models
from student.models import Student
from teacher.models import Teacher
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Course(models.Model):
    course_code = models.CharField(max_length=20, null=False, primary_key=True, blank=False)
    course_name = models.CharField(default='Course name', max_length=50, null=False)
    start_day = models.DateTimeField(null=True)
    end_day = models.DateTimeField(null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student, blank=True)

    MON = '2'
    TUE = '3'
    WED = '4'
    THU = '5'
    FRI = '6'
    SAT = '7'
    class_time_choices = [
        (MON, 'Monday'),
        (TUE, 'Tuesday'),
        (WED, 'Wednesday'),
        (THU, 'Thursday'),
        (FRI, 'Friday'),
        (SAT, 'Saturday'),
    ]
    class_time = models.CharField(
        choices=class_time_choices,
        default=MON,
        max_length=3
    )
    FIRST = '1'
    SECOND = '2'
    THIRD = '3'
    FOURTH = '4'
    FIFTH = '5'
    SIXTH = '6'
    SEVENTH = '7'
    EIGHTH = '8'
    NINTH = '9'
    TENTH = '10'

    class_time_calendar_choices = [
        (FIRST, 'FIRST'),
        (SECOND, 'SECOND'),
        (THIRD, 'THIRD'),
        (FOURTH, 'FOURTH'),
        (FIFTH, 'FIFTH'),
        (SIXTH, 'SIXTH'),
        (SEVENTH, 'SEVENTH'),
        (EIGHTH, 'EIGHTH'),
        (NINTH, 'NINTH'),
        (TENTH, 'TENTH'),
    ]
    class_time_calendar = models.CharField(
        choices=class_time_calendar_choices,
        default=FIRST,
        max_length=10
    )
    class_time_begin_time = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

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
