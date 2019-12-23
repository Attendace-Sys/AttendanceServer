from rest_framework import serializers
from .models import Course, Schedule, Attendance, ScheduleImagesData
from student.models import Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'teacher_code', 'teacher_image']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class StudentCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ['student_code', 'first_name', ]
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentCustomSerializer()

    class Meta:
        model = Attendance
        fields = ['attendance_code', 'schedule_code', 'absent_status', 'image_data', 'student']


class ScheduleImagesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleImagesData
        fields = '__all__'
