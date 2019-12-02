from django.shortcuts import render
from rest_framework import viewsets
from .models import Course
from django.http import HttpResponse
from .serializers import CourseSerializer


# Create your views here.

class TeacherView(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('teacher_code')
    serializer_class = CourseSerializer


def teacher_show(request):
    if request.method == 'GET':
        courses = Course.objects.all().order_by('teacher_code')
        courses_serializer = CourseSerializer(courses, many=True)
        return HttpResponse(status=HttpResponse.status_code)
    elif request.method == 'POST':
        courses_data = HttpResponse(request)
        courses_serializer = CourseSerializer(data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return HttpResponse(status=HttpResponse.status_code)
        return HttpResponse(status=HttpResponse.status_code)
