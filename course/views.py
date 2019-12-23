from django.shortcuts import render
from rest_framework import viewsets
from .models import Course, Schedule, Attendance, ScheduleImagesData
from student.models import Student, StudentImagesData
from django.http import HttpResponse
from .serializers import CourseSerializer, ScheduleSerializer, ScheduleImagesDataSerializer, StudentCustomSerializer, \
    AttendanceSerializer
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
from course.forms import ScheduleForms
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods


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
            return Response({"classes": serializer.data}, status=200)
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
            return Response({'schedule': serializer.data}, status=200)
        else:
            schedule = Schedule.objects.filter()
            serializer = ScheduleSerializer(schedule, many=True)
            return Response({'schedule': serializer.data}, status=200)


class AttendanceListViewAPI(generics.ListAPIView,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    queryset = Attendance.objects.all()
    serializer_class = StudentCustomSerializer
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
        json_data = json.loads(json.dumps(data))
        count = 0
        for item in json_data['data']:
            Attendance.objects.filter(attendance_code=item['attendance_code']).update(
                absent_status=item['absent_status'])
            count = count + 1

        if count == 0:
            return Response({'message': 'failed'}, status=401)

        return Response({'message': 'suceess'}, status=200)


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
            return Response({'attends': serializer.data}, status=200)
        else:
            attendance = Attendance.objects.filter()
            serializer = AttendanceSerializer(attendance, many=True)

            return Response({'attends': serializer.data}, status=200)


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
            return Response({'attends': serializer.data}, status=200)
        else:
            schedule_image_data = ScheduleImagesData.objects.filter()
            serializer = ScheduleImagesDataSerializer(schedule_image_data, many=True)
            return Response({'attends': serializer.data}, status=200)


class UploadCheckingAttendanceViewAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        data = request.data
        json_data = json.loads(json.dumps(data))
        count = 0
        for item in json_data['data']:
            Attendance.objects.filter(attendance_code=item['attendance_code']).update(
                absent_status=item['absent_status'])
            count = count + 1

        if count == 0:
            return Response({'message': 'failed'}, status=401)

        return Response({'message': 'suceess'}, status=200)


class ScheduleView(CreateView):
    queryset = Schedule.objects.all()
    model = Schedule
    form_class = ScheduleForms
    template_name = 'schedule_form.html'
    success_url = 'serializer/schedules'


def schedule_list(request, template_name='schedule_list.html'):
    if request.user.is_superuser:
        schedule = Schedule.objects.all()
    else:
        schedule = Schedule.objects.filter()
    data = {'object_list': schedule}
    return render(request, template_name, data)

from django.utils.datastructures import MultiValueDict


@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST"])
def schedule_create(request, template_name='schedule_form.html'):

    if (request.method== 'POST'):

        form = ScheduleForms(request.POST or None, request.FILES or None)

        # boundingBox in class room images
        m_json_data = form.data.getlist('json_data')[0]

        # class room images
        in_memory_uploaded_file_data = request.FILES.getlist('files')
        

        for file in in_memory_uploaded_file_data:
            print(file)

        # extract all faces in classroom images


        # build vectors for all faces in classroom images


        # get all list stutdent in class
        m_schedule_code = form.data.getlist('schedule_code')[0]
        course_id = list(Schedule.objects.filter(schedule_code = m_schedule_code).values('course')) [0]
        list_student = list(Student.objects.filter(course__course_code=course_id['course']))

        # get all images of each student in class
        for item in list_student:
            list_image = list(StudentImagesData.objects.filter(student_id = item.student).values('image_data'))

        # build vector for all faces images of student in class


        # use knn for detect faces (label, prob)


        # build json to return
        json_response = '' 


        return HttpResponse(json_response, content_type='application/json')

    else:
        return HttpResponse('error', content_type='application/json')





def schedule_update(request, schedule_code, template_name='schedule_form.html'):
    if request.user.is_superuser:
        schedule = get_object_or_404(Schedule, schedule_code=schedule_code)
    else:
        schedule = get_object_or_404(Schedule, schedule_code=schedule_code)
    form = ScheduleForms(request.POST or None, request.FILES or None, instance=schedule)
    if form.is_valid():
        form.save()
        return redirect('schedule:schedule_list')
    return render(request, template_name, {'form': form})


class ScheduleImagesDataView(viewsets.ModelViewSet):
    queryset = ScheduleImagesData.objects.all()
    serializer_class = ScheduleImagesDataSerializer


class ScheduleSerializerView(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
