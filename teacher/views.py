from django.shortcuts import render
from rest_framework import viewsets
from .models import Teacher
from django.http import HttpResponse
from .serializers import TeacherSerializer

# Create your views here.


class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('teacher_code')
    serializer_class = TeacherSerializer


def teacher_show(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all().order_by('teacher_code')
        teachers_serializer = TeacherSerializer(teachers, many=True)
        return HttpResponse(status=HttpResponse.status_code)
    elif request.method == 'POST':
        teacher_data = HttpResponse(request)
        teacher_serializer = TeacherSerializer(data=teacher_data)
        if teacher_serializer.is_valid():
            teacher_serializer.save()
            return HttpResponse(status=HttpResponse.status_code)
        return HttpResponse(status=HttpResponse.status_code)
