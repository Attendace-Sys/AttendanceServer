from django.db import models
from student.models import Student
from teacher.models import Teacher
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from datetime import timedelta
from DjangoAPI import settings


# Create your models here.

class Course(models.Model):
    course_code = models.CharField(max_length=20, null=False, primary_key=True, blank=False)
    course_name = models.CharField(max_length=50, null=False)
    course_room = models.CharField(max_length=50, null=False)
    start_day = models.DateField(null=True)
    end_day = models.DateField(null=True)
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

    def create_attendance(self, schedule, *args, **kwargs):
        for student in self.students.all():
            attendance = Attendance()
            attendance.attendance_code = schedule.schedule_code + '-' + student.student_code
            attendance.student = student
            attendance.schedule_code = schedule
            attendance.absent_status = False
            attendance.checked_status = False
            attendance.image_data = None
            attendance.save()

    def create_schedule(self, *args, **kwargs):
        # get begin day
        day_begin = self.start_day
        day_end = self.end_day
        day_of_week = int(self.day_of_week)
        time_start_of_course = self.time_start_of_course
        time_duration = self.time_duration
        date = day_begin
        if date.weekday() <= day_of_week:
            date = date + timedelta(days=(day_of_week - date.weekday()))
        else:
            date = date + timedelta(days=(7 - (date.weekday() - day_of_week)))
        begin = date
        # get end day
        date = day_end
        if date.weekday() >= day_of_week:
            date = date - timedelta(days=(day_of_week - date.weekday()))
        else:
            date = date - timedelta(days=(7 - (day_of_week - date.weekday())))
        end = date
        # create schedule
        schedule_number_of_day_count = 1
        date_schedule = begin
        while date_schedule <= end:
            schedule = Schedule(course=self)
            schedule.schedule_code = \
                self.course_code + "-" + str(schedule_number_of_day_count)
            schedule.date_schedule = date_schedule
            schedule.schedule_number_of_day = schedule_number_of_day_count
            schedule_number_of_day_count = schedule_number_of_day_count + 1
            if schedule.schedule_date is None:
                schedule.schedule_date = date_schedule
            schedule.save()
            self.create_attendance(schedule, *args, **kwargs)
            date_schedule = date_schedule + timedelta(days=7)

    def save(self, *args, **kwargs):
        instance = super(Course, self).save(*args, **kwargs)
        if self.pk:
            # do when create
            if self.start_day is not None and self.end_day is not None and (self.start_day <= self.end_day):
                self.create_schedule(*args, **kwargs)
        return instance

    def __init__(self, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)
        if self.start_day is not None and self.end_day is not None and (self.start_day <= self.end_day):
            self.create_schedule(*args, **kwargs)

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name_plural = 'Quản lý Lớp học'


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    schedule_code = models.CharField(max_length=30, null=False, primary_key=True)
    schedule_date = models.DateField(auto_now_add=True, null=True)
    schedule_number_of_day = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = 'Quản lý buổi học'

    def save(self, *args, **kwargs):
        super(Schedule, self).save(*args, **kwargs)

    def __str__(self):
        return self.schedule_code


class Attendance(models.Model):
    attendance_code = models.CharField(max_length=50, null=False, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    schedule_code = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=False)
    absent_status = models.BooleanField(default=False)

    # save to student_name folder

    def path_and_rename(self, name):
        # get filename
        filename = 'students/{0}/images/{1}'.format(self.student, self.image_data.name)
        # return the whole path to the file
        return filename

    image_data = models.FileField(upload_to=path_and_rename, null=True)

    @property
    def date(self):
        if self.schedule_code.schedule_date is None:
            return None
        return self.schedule_code.schedule_date

    def save(self, *args, **kwargs):
        super(Attendance, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quản lý điểm danh'


class ScheduleImagesData(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=False)

    def path_and_rename(self, name):
        # get filename course_code = list(Schedule.objects.filter(schedule_code=self.schedule).values_list(
        # 'course__course_code', flat=True).distinct())[0]
        course_code, schedule_number_of_day = list(
            Schedule.objects.filter(schedule_code=self.schedule).values_list('course__course_code',
                                                                             'schedule_number_of_day').distinct())[0]
        filename = 'schedule/{0}/{1}/{2}'.format(course_code, schedule_number_of_day, self.image_data.name)
        # return the whole path to the file
        return filename

    image_data = models.FileField(upload_to=path_and_rename, blank=False, null=False)
    image_date_upload = models.DateField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        super(ScheduleImagesData, self).save(*args, **kwargs)

    def __str__(self):
        return self.image_data.name
