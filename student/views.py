from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .models import StudentImagesData, Student
from django.http import HttpResponse
from rest_framework.parsers import FormParser
from django.http.multipartparser import MultiPartParser
from student.forms import StudentForms, StudentImagesDataForms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
import json
from .serializers import StudentImagesDataSerializer, StudentSerializer
from rest_framework.views import APIView
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.views.generic.edit import CreateView
from rest_framework import status
from rest_framework import generics
# from .serializers import EmployeeSerializer
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.core import serializers

import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods


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


class StudentView(CreateView):
    queryset = Student.objects.all()
    model = Student
    form_class = StudentForms
    template_name = 'student_form.html'
    success_url = 'serializer/students'


def student_list(request, template_name='student_list.html'):
    if request.user.is_superuser:
        student = Student.objects.all()
    else:
        student = Student.objects.filter()
    data = {'object_list': student}
    return render(request, template_name, data)


@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST", "GET"])
def student_create_or_update(request, student_code=None, template_name='student_form.html'):
    if student_code is None:
        # if no have code link =>
        students = Student.objects.get(student_code=student_code)
        print(type(students))
        #

        form = StudentForms(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('student:student_list')
        return render(request, template_name, {'form': form})
    else:
        student = get_object_or_404(Student, student_code=student_code)
        form = StudentForms(request.POST or None, request.FILES or None, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student:student_list')
        return render(request, template_name, {'form': form})


def student_create(request, template_name='student_form.html'):
    form = StudentForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('student:student_list')
    return render(request, template_name, {'form': form})


def student_update(request, student_code, template_name='student_form.html'):
    if request.user.is_superuser:
        student = get_object_or_404(Student, student_code=student_code)
    else:
        student = get_object_or_404(Student, student_code=student_code)
    form = StudentForms(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student:student_list')
    return render(request, template_name, {'form': form})


def student_delete(request, student_code, template_name='student_confirm_delete.html'):
    if request.user.is_superuser:
        student = get_object_or_404(Student, student_code=student_code)
    else:
        student = get_object_or_404(Student, student_code=student_code)
    if request.method == 'POST':
        student.delete()
        return redirect('student:student_list')
    return render(request, 'student_form.html', {'form': form})


# from django_filters import FilterSet
# from django_filters import rest_framework as filters
# Create your views here.


class StudentListViewAPI(generics.ListAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'student_code'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, student_code=None):
        if student_code:
            return self.retrieve(request, student_code)
        else:
            return self.list(request)

    def post(self, request, course_code=None):
        return self.create(request)

    def perform_create(self, serializer):
        # modifier save
        serializer.save()

    def perform_update(self, serializer):
        # modifier save
        serializer.save()

    def put(self, request, student_code=None):
        return self.update(request, student_code)

    def delete(self, request, student_code=None):
        return self.destroy(request, student_code)

    # def get_queryset(self, type, code):
    #    user = self.request.user
    #    return user.accounts.all()


class StudentListViewByStudentAPI(generics.ListAPIView,
                                  mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'student_code'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, student_code=None):
        if student_code:
            student = Student.objects.filter(student_code=student_code)
            serializer = StudentSerializer(student, many=True)
            return Response(serializer.data, status=200)
        else:
            return self.list(request)


class StudentImagesDataListViewAPI(generics.ListAPIView,
                                   mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin):
    queryset = StudentImagesData.objects.all()
    serializer_class = StudentImagesDataSerializer
    # lookup_field = 'student_code'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        else:
            return self.list(request)

    def post(self, request, course_code=None):
        return self.create(request)

    def perform_create(self, serializer):
        # modifier save
        serializer.save()

    def perform_update(self, serializer):
        # modifier save
        serializer.save()

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

    # def get_queryset(self, type, code):
    #    user = self.request.user
    #    return user.accounts.all()


class StudentImagesDataListViewByStudentAPI(generics.ListAPIView,
                                            mixins.ListModelMixin,
                                            mixins.CreateModelMixin,
                                            mixins.RetrieveModelMixin,
                                            mixins.UpdateModelMixin,
                                            mixins.DestroyModelMixin):
    queryset = StudentImagesData.objects.all()
    serializer_class = StudentImagesDataSerializer
    lookup_field = 'student'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, student=None):
        if student:
            courses = StudentImagesData.objects.filter(student=student)
            serializer = StudentImagesDataSerializer(student, many=True)
            return Response(serializer.data, status=200)
        else:
            return self.list(request)


class StudentGetListCourseByStudentAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, student):
        if student:
            students = list(Student.objects.get(student_code=student).course_set.all().values('course_code',
                                                                                              'course_name', 'teacher',
                                                                                              'teacher',
                                                                                              'teacher__first_name'))
            json_file = json.dumps(students, ensure_ascii=False).encode('utf8')
            return HttpResponse(json_file, content_type='application/json', status=200)
        return Response({'message': 'failed'}, status=401)


from course.models import Schedule, Attendance


class StudentAttendanceOfACourse(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, course_code=None, student_code=None):
        if course_code:
            list_schedule_code = list(Schedule.objects.filter(course=course_code).values('schedule_code'))
            list_attendance = []
            for item in list_schedule_code:
                attendance = list(Attendance.objects.filter(schedule_code=item.get('schedule_code')).filter(
                    student=student_code).values('attendance_code', 'schedule_code', 'schedule_code__schedule_date',
                                                 'absent_status'))[0]

                list_attendance.append(attendance)
                print(type(list_attendance))

            return Response(list_attendance, status=200)
        return Response({'message': 'failed'}, status=401)