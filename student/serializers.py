from rest_framework import serializers
from .models import Student
from .models import StudentImagesData
from . import models


class StudentImagesDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentImagesData
        fields = ['student', 'image_data']


class StudentSerializer(serializers.ModelSerializer):
    images = StudentImagesDataSerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = ['student_code','first_name',
                'last_name', 'email',
                'student_video_data', 'images',
                'username',
                'password', ]
        # fields ='__all__'

    def create(self, validated_data):
        # return Student.objects.create(**validated_data)

        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):
        images = validated_data.pop('images')
        # return super().update(instance, validated_data)
        instance.student_code = validated_data.get("student_code", instance.student_code)
        instance.student_video_data = validated_data.get("student_video_data", instance.student_video_data)
        instance.save()
        images_choices = []
        existing_ids =[c.id for c in  instance.images]
        for image in images:
            if "id" in image.key():
                if StudentImagesData.objects.filter(id = image["id"]).exists():
                    c = StudentImagesData.object.get(id = image["id"])
                    c.image_data = image.get("image_data")
                    c.image_name = image.get("image_name")
                    c.save()
                    images_choices.append(c)
                else:
                    continue
            else:
                c = StudentImagesData.objects.create(**image, student=student)
                images_choices.append(c.id)
        for image in instance.images:
            if image.id not in images_choices:
                image.delete()
        return instance