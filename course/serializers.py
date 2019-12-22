from rest_framework import serializers
from .models import Course, Schedule, Attendance, ScheduleImagesData


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'teacher_code', 'teacher_image']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class ScheduleImagesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleImagesData
        fields = '__all__'
