from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'teacher_code', 'teacher_image']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)