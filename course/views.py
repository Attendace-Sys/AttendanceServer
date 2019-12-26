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
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from course.forms import ScheduleForms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from PIL import Image
import io
import json
from keras.models import load_model
import os
import course.apps as app
import keras
import numpy as np
from random import choice
from numpy import load
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import NearestNeighbors
from course.label_encoder_ext import LabelEncoderExt
from django.utils.datastructures import MultiValueDict
from numpy import asarray
import json
from PIL import ImageOps
import PIL
from numpy import load
from numpy import expand_dims
from numpy import asarray
import tensorflow as tf
from sklearn import preprocessing
import numpy as np
from keras.models import Model, Sequential
from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
from PIL import Image
from keras.preprocessing.image import load_img, save_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
from keras.models import model_from_json
from os import listdir
from keras.applications.imagenet_utils import preprocess_input
from os import listdir
from os.path import isdir


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


def l2_normalize(x):
    return x / np.sqrt(np.sum(np.multiply(x, x)))


def get_list_of_list_face_vector_in_class_imgs(in_memory_uploaded_file_data, m_json_data, model):
    required_size = (160, 160)

    index = 0
    list_of_list_face_in_each_img = []
    for file in in_memory_uploaded_file_data:

        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)

        list_face_array_in_img = []

        list_face_rect_in_img = m_json_data[index]['face_rect']
        for rect in list_face_rect_in_img:
            x1 = rect['left']
            x2 = rect['right']
            y1 = rect['top']
            y2 = rect['bottom']
            box = (x1, y1, x2, y2)

            resized_img = image.crop(box)
            resized_img = resized_img.resize(required_size, Image.ANTIALIAS)
            img = img_to_array(resized_img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)

            with app.graph.as_default():
                img_vector = l2_normalize(model.predict(img)[0, :])
                list_face_array_in_img.append(img_vector)

        list_of_list_face_in_each_img.append(list_face_array_in_img)
        index = index + 1

    return list_of_list_face_in_each_img


def preprocess_image(image_path):
    img = load_img(image_path, target_size=(160, 160))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # preprocess_input normalizes input in scale of [-1, +1]. You must apply same normalization in prediction.
    # Ref: https://github.com/keras-team/keras-applications/blob/master/keras_applications/imagenet_utils.py (Line 45)
    img = preprocess_input(img)
    return img


# load images and extract faces for all images in a directory
def load_faces(directory, model):
    faces = list()
    # enumerate files
    for filename in listdir(directory):
        # path
        path = directory + filename
        # get face
        img = preprocess_image(path)
        with app.graph.as_default():
            img_vector = l2_normalize(model.predict(img)[0, :])
            faces.append(img_vector)

    return faces


def load_student_trainX_trainY(list_student, model, STUDENT_IMG_DIR):
    train_X = []
    train_Y = []

    for student in list_student:
        student_code = student.student_code
        # print (student_code)
        student_img_folder = STUDENT_IMG_DIR + student_code + "/images/"
        # skip any files that might be in the dir
        if not isdir(student_img_folder):
            continue

        # load all faces in the subdirectory
        faces = load_faces(student_img_folder, model)
        # create labels
        labels = [student_code for _ in range(len(faces))]

        train_X.extend(faces)
        train_Y.extend(labels)

    return train_X, train_Y


def findEuclideanDistance(source_representation, test_representation):
    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance


@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST"])
def schedule_create(request, template_name='schedule_form.html'):
    if request.method == 'POST':

        form = ScheduleForms(request.POST or None, request.FILES or None)
        # boundingBox in class room images
        m_json_str = form.data.getlist('json_data')[0]
        m_json_data = json.loads(m_json_str)

        model = app.keras_model

        # class room images
        in_memory_uploaded_file_data = request.FILES.getlist('files')

        # extract all faces in classroom images
        list_of_list_face_vector_in_each_img = get_list_of_list_face_vector_in_class_imgs(in_memory_uploaded_file_data,
                                                                                          m_json_data, model)

        # get all list stutdent in class
        m_schedule_code = form.data.getlist('schedule_code')[0]
        course_id = list(Schedule.objects.filter(schedule_code=m_schedule_code).values('course'))[0]
        list_student = list(Student.objects.filter(course__course_code=course_id['course']))

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        STUDENT_IMG_DIR = BASE_DIR + '/media/students/'

        # build vectors for all faces in classroom images
        trainX, trainY = load_student_trainX_trainY(list_student, model, STUDENT_IMG_DIR)
        print(trainY)

        # label encode targets
        out_encoder = LabelEncoderExt()
        out_encoder.fit(trainY)
        trainY = out_encoder.transform(trainY)

        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(trainX)

        list_predict_result = []

        imag_count = 0
        # Threshold see: https://sefiks.com/2018/09/03/face-recognition-with-facenet-in-keras/
        distance_threshold = 0.35
        for face_vector_list in list_of_list_face_vector_in_each_img:
            neigh_dist, neigh_ind = neigh.kneighbors(face_vector_list, n_neighbors=1)
            print(neigh_dist)
            print(neigh_ind)

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
        return redirect('schedule:schedule_form')
    return render(request, template_name, {'form': form})


class ScheduleImagesDataView(viewsets.ModelViewSet):
    queryset = ScheduleImagesData.objects.all()
    serializer_class = ScheduleImagesDataSerializer


class ScheduleSerializerView(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


