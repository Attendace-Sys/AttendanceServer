from django.shortcuts import render
from rest_framework import viewsets
from .models import Course, Schedule, Attendance, ScheduleImagesData
from django.http import HttpResponse
from .serializers import CourseSerializer, ScheduleSerializer, AttendanceSerializer, ScheduleImagesDataSerializer
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

import json

# from django_filters import FilterSet
# from django_filters import rest_framework as filters
# Create your views here.


class CourseListViewAPI(generics.ListAPIView,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'course_code'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, course_code=None):
        if course_code:
            return self.retrieve(request, course_code)
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

    def put(self, request, course_code=None):
        return self.update(request, course_code)

    def delete(self, request, course_code=None):
        return self.destroy(request, id)

    # def get_queryset(self, type, code):
    #    user = self.request.user
    #    return user.accounts.all()


class CourseListViewByTeacherAPI(generics.ListAPIView,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'teacher'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, teacher=None):
        if teacher:
            courses = Course.objects.filter(teacher=teacher)
            serializer = CourseSerializer(courses, many=True)
            return Response({"classes":serializer.data}, status=200)
        else:
            return self.list(request)


class ScheduleListViewAPI(generics.ListAPIView,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = 'schedule_code'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, schedule_code=None):
        if schedule_code:
            return self.retrieve(request, schedule_code)
        else:
            return self.list(request)

    def post(self, request, schedule_code=None):
        return self.create(request)

    def perform_create(self, serializer):
        # modifier save
        serializer.save()

    def perform_update(self, serializer):
        # modifier save
        serializer.save()

    def put(self, request, schedule_code=None):
        return self.update(request, schedule_code)

    def delete(self, request, schedule_code=None):
        return self.destroy(request, id)


class ScheduleListViewByCourseAPI(generics.ListAPIView,
                                  mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = 'course'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, course=None):
        if course:
            schedule = Schedule.objects.filter(course=course)
            serializer = ScheduleSerializer(schedule, many=True)
            return Response({'schedule':serializer.data}, status=200)
        else:
            schedule = Schedule.objects.filter()
            serializer = ScheduleSerializer(schedule, many=True)
            return Response({'schedule':serializer.data}, status=200)


class AttendanceListViewAPI(generics.ListAPIView,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    lookup_field = 'attendance_code'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, attendance_code=None):
        if attendance_code:
            return self.retrieve(request, attendance_code)
        else:
            return self.list(request)

    def post(self, request, attendance_code=None):
        return self.create(request)

    def perform_create(self, serializer):
        # modifier save
        serializer.save()

    def perform_update(self, serializer):
        # modifier save
        serializer.save()

    def put(self, request, attendance_code=None):
        return self.update(request, attendance_code)

    def delete(self, request, attendance_code=None):
        return self.destroy(request, id)

class UpdateListAttendancesViewAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        data = request.data
        print(data)
        jsonData = json.loads( json.dumps(data))
        print(jsonData)
        schedule_code = jsonData['schedule_code']
        print(schedule_code)
        count = 0
        for item in jsonData['data']:
            Attendance.objects.filter(attendance_code=item['attendance_code']).update(absent_status=item['absent_status'])
            count = count + 1

        if count == 0:        
            return Response({'message':'failed'}, status=401)
               
        return Response({'message':'suceess'}, status=200)


class AttendanceListViewByStudentAPI(generics.ListAPIView,
                                     mixins.ListModelMixin,
                                     mixins.CreateModelMixin,
                                     mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    lookup_field = 'student'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, student=None):
        if student:
            attendance = Attendance.objects.filter(student=student)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data, status=200)
        else:
            return self.list(request)


class AttendanceListViewByScheduleAPI(generics.ListAPIView,
                                      mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    lookup_field = 'schedule_code'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, schedule_code=None):
        if schedule_code:
            attendance = Attendance.objects.filter(schedule_code=schedule_code)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response({'attends':serializer.data}, status=200)
        else:
            attendance = Attendance.objects.filter()
            serializer = AttendanceSerializer(attendance, many=True)
            
            return Response({'attends':serializer.data}, status=200)


class ScheduleImagesDataListViewByScheduleAPI(generics.ListAPIView,
                                              mixins.ListModelMixin,
                                              mixins.CreateModelMixin,
                                              mixins.RetrieveModelMixin,
                                              mixins.UpdateModelMixin,
                                              mixins.DestroyModelMixin):
    queryset = ScheduleImagesData.objects.all()
    serializer_class = ScheduleImagesDataSerializer
    lookup_field = 'schedule'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, schedule=None):
        if schedule:
            schedule_image_data = ScheduleImagesData.objects.filter(schedule=schedule)
            serializer = ScheduleImagesDataSerializer(schedule_image_data, many=True)
            return Response({'attends':serializer.data}, status=200)
        else:
            schedule_image_data = ScheduleImagesData.objects.filter()
            serializer = ScheduleImagesDataSerializer(schedule_image_data, many=True)
            return Response({'attends':serializer.data}, status=200)



"""
class CourseViewAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)


class CourseDetailView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, course_code):
        try:
            return Course.objects.get(course_code=course_code)
        except Course.DoesNotExist as e:
            return Response({"error": "Given Course code not found."}, status=404)

    def get(self, request, course_code=None):
        instance = self.get_object(course_code)
        serializer = CourseSerializer(instance)
        return Response(serializer.data)

    def get(self, request, teacher_code=None):
        instance = self.get_object(teacher_code)
        serializer = CourseSerializer(instance)
        return Response(serializer.data)

    def put(self, request, course_code=None):
        data = request.data
        instance = self.get_object(course_code)
        serializer = CourseSerializer(instance, data=data)
        if serializer.is_valide():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.erros, status=400)

    def delete(self, request, course_code=None):
        instance = self.get_object(course_code)
        instance.delete()
        return HttpResponse(status=204)




class CourseListView(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('teacher')
    serializer_class = CourseSerializer
"""
