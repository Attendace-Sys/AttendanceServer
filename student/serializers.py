from rest_framework import serializers
from .models import Student
from .models import StudentImagesData
from . import models
from multiupload.fields import MultiFileField


class StudentImagesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentImagesData
        # fields = ['image_code', 'student', 'image_data', 'image_date_upload']
        fields = ['student', 'image_data', 'image_date_upload', ]

    def create(self, validated_data):
        return StudentImagesData.objects.create(**validated_data)


class StudentSerializer(serializers.ModelSerializer):
    # files = MultiFileField(min_num=1, max_num=15, max_file_size=1024*1024*5)
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        return Student.objects.create(**validated_data)


class StudentCustomSerializer(serializers.ModelSerializer):
    # files = MultiFileField(min_num=1, max_num=15, max_file_size=1024*1024*5)
    class Meta:
        model = Student
        fields = ['student_code', 'first_name', 'email', 'username', 'password', 'student_video_data']

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
