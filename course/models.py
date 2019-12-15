from django.db import models
from student.models import Student
from teacher.models import Teacher
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Course(models.Model):
    course_code = models.CharField(max_length=20, null=False, primary_key=True, blank=False)
    course_name = models.CharField(max_length=50, null=False)
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
    SUN = '8'
    """
    day_of_week_choices = [
        (MON, 'Monday'),
        (TUE, 'Tuesday'),
        (WED, 'Wednesday'),
        (THU, 'Thursday'),
        (FRI, 'Friday'),
        (SAT, 'Saturday'),
    ]
    """
    day_of_week_choices = [
        (MON, 'Thứ hai'),
        (TUE, 'Thứ ba'),
        (WED, 'Thứ tư'),
        (THU, 'Thứ năm'),
        (FRI, 'Thứ sáu'),
        (SAT, 'Thứ bảy'),
        (SUN, 'Chủ nhật'),
    ]
    day_of_week = models.CharField(
        choices=day_of_week_choices,
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

    time_start_of_course_choices = [
        (FIRST, 'Tiết 1'),
        (SECOND, 'Tiết 2'),
        (THIRD, 'Tiết 3'),
        (FOURTH, 'Tiết 4'),
        (FIFTH, 'Tiết 5'),
        (SIXTH, 'Tiết 6'),
        (SEVENTH, 'TIết 7'),
        (EIGHTH, 'Tiết 8'),
        (NINTH, 'Tiết 9'),
        (TENTH, 'Tiết 10'),
    ]
    time_start_of_course = models.CharField(
        choices=time_start_of_course_choices,
        default=FIRST,
        max_length=10
    )
    time_duration = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name_plural = 'Quản lý Lớp học'


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    schedule_code = models.CharField(max_length=20, null=False, primary_key=True)
    schedule_date = models.DateTimeField(auto_now_add=True, null=False)
    schedule_number_of_day = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = 'Quản lý buổi học'


class Attendance(models.Model):
    attendance_code = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    schedule_code = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=False)
    absent_status = models.BooleanField(default=False)
    # save to student_name folder
    image_data = models.FileField(upload_to='media/students/images/}', blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Quản lý điểm danh'


class ScheduleImagesData(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=False)
    """
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
    """
    # save picture to student folder
    image_data = models.FileField(upload_to='media/', blank=False, null=False)
    image_date_upload = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        super(ScheduleImagesData, self).save(*args, **kwargs)

    def __str__(self):
        return self.image_data.name
