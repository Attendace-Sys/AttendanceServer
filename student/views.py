from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .models import StudentImagesData
from django.http import HttpResponse
from .serializers import StudentSerializer
from .serializers import StudentImagesDataSerializer
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from django.http.multipartparser import MultiPartParser
from . import helpers


# Create your views here.

class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('student_code')
    serializer_class = StudentSerializer


def student_show(request):
    if request.method == 'GET':
        students = Student.objects.all().order_by('student_code')
        students_serializer = StudentSerializer(students, many=True)
        return HttpResponse(status=HttpResponse.status_code)
    elif request.method == 'POST':
        students_data = HttpResponse(request)
        students_serializer = StudentSerializer(data=students_data)
        if students_serializer.is_valid():
            students_serializer.save()
            return HttpResponse(status=HttpResponse.status_code)
        return HttpResponse(status=HttpResponse.status_code)


class StudentImagesDataView(viewsets.ModelViewSet):
    queryset = StudentImagesData.objects.all()
    serializer_class = StudentImagesDataSerializer

def FaceVideo_show(request):
    if request.method == 'GET':
        face_images = StudentImagesData.objects.all()
        face_images_serializer = StudentImagesDataSerializer(face_images, many=True)
        return HttpResponse(status=HttpResponse.status_code)
    elif request.method == 'POST':
        face_images_data = HttpResponse(request)
        face_images_serializer = StudentImagesDataSerializer(data=face_images_data)
        if face_images_serializer.is_valid():
            face_images_serializer.save()
            return HttpResponse(status=HttpResponse.status_code)
        return HttpResponse(status=HttpResponse.status_code)
