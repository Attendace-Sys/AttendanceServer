from rest_framework import serializers
from .models import Teacher


# -*- coding: utf-8 -*-

class TeacherSerializer(serializers.ModelSerializer):
    """
    Because 'Teacher' is a reverse relationship on the User model,
    it will not be included by default when using the ModelSerializer class,
    so we needed to add an explicit field for it.
    """

    class Meta:
        model = Teacher
        # fields = '__all__'
        fields = ['teacher_code', 'first_name', 'last_name', 'email', 'teacher_image', 'username', 'password',
                  'date_joined']

    @staticmethod
    def create(validated_data):
        return Teacher.objects.create(**validated_data)
