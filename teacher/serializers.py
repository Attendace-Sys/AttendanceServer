from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    """
    Because 'Teacher' is a reverse relationship on the User model,
    it will not be included by default when using the ModelSerializer class,
    so we needed to add an explicit field for it.
    """

    class Meta:
        model = Teacher
        fields = '__all__'
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'teacher_code', 'teacher_image']

    def create(self, validated_data):
        return Teacher.objects.create(**validated_data)