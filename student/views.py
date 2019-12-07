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
from student.forms import StudentForms, StudentImagesDataForms
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404

# -*- coding: utf-8 -*-
# Create your views here.
class StudentSerializerView(viewsets.ModelViewSet):
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


@method_decorator(csrf_exempt, name='dispatch')
class StudentView(CreateView):
    queryset = Student.objects.all()
    model = Student
    form_class = StudentForms
    template_name = 'student_form.html'
    success_url = 'serializer/students'

@method_decorator(csrf_exempt, name='dispatch')
@login_required
def student_list(request, template_name='student_list.html'):
    if request.user.is_superuser:
        student = Student.objects.all()
    else:
        student = Student.objects.filter(user=request.user)
    data = {}
    data['object_list'] = student
    return render(request, template_name, data)

@method_decorator(csrf_exempt, name='dispatch')
@login_required
def student_create(request, template_name='student_form.html'):
    form = StudentForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('student:student_list')
    return render(request, template_name, {'form':form})
 
@method_decorator(csrf_exempt, name='dispatch')
@login_required
def student_update(request, student_code, template_name='student_form.html'):
    if request.user.is_superuser:
        student= get_object_or_404(Student, student_code=student_code)
    else:
        student= get_object_or_404(Student, student_code=student_code, user=request.user)
    form = StudentForms(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student:student_list')
    return render(request, template_name, {'form':form})

@method_decorator(csrf_exempt, name='dispatch')
@login_required
def student_delete(request, student_code, template_name='student_confirm_delete.html'):
    if request.user.is_superuser:
        student= get_object_or_404(Student, student_code=student_code)
    else:
        student= get_object_or_404(Student, student_code=student_code, user=request.user)
    if request.method=='POST':
        student.delete()
        return redirect('student:student_list')
    return render(request, template_name, {'object':student})
