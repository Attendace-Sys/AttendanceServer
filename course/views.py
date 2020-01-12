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
# from keras.models import load_model
import os
import course.apps as app
# import keras
import numpy as np
from random import choice
from numpy import load
from numpy import expand_dims
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import Normalizer
# from sklearn.neighbors import NearestNeighbors
# from course.label_encoder_ext import LabelEncoderExt
# from django.utils.datastructures import MultiValueDict
from numpy import asarray
import json
from PIL import ImageOps
import PIL
from numpy import load
from numpy import expand_dims
from numpy import asarray
# import tensorflow as tf
# from sklearn import preprocessing
import numpy as np
# from keras.models import Model, Sequential
# from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
from PIL import Image
# from keras.preprocessing.image import load_img, save_img, img_to_array
# from keras.applications.imagenet_utils import preprocess_input
# from keras.preprocessing import image
# from keras.models import model_from_json
from os import listdir
# from keras.applications.imagenet_utils import preprocess_input
from os import listdir
from os.path import isdir
import numpy as np
import face_recognition
# from keras.preprocessing.image import load_img
import random


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
    queryset = Course.objects.filter()
    serializer_class = CourseSerializer
    lookup_field = 'teacher'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, teacher=None):
        return self.update(request, teacher)

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


# API GET list student of a course
class ListStudentOfCourseViewAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, course_code=None):
        if course_code:
            list_student = Course.objects.filter(course_code=course_code).values('students__student_code',
                                                                                 'students__first_name')
            # list_student = Course.objects.filter(course_code = course_code).annotate(student_code =
            # 'students__student_code', student_name'students__first_name')

            # list_schedule = Schedule.objects.filter(course = course_code).values('schedule_code'))
            list_schedule = list(Schedule.objects.filter(course=course_code).values_list('schedule_code'))

            list_schedule_code = []
            for item in list_schedule:
                list_schedule_code.append(item[0])
            # print(list_schedule_code)

            index = 0
            for student in list_student:
                num_present = 0;
                num_absent = 0;
                list_attendance = Attendance.objects.filter(student=student.get('students__student_code')).filter(
                    schedule_code__in=list_schedule_code).values_list('absent_status')
                for item in list_attendance:
                    if (item[0] == True):
                        num_present = num_present + 1
                    else:
                        num_absent = num_absent + 1

                list_student[index].update({'num_present': num_present})
                list_student[index].update({'num_absent': num_absent})

                index = index + 1

            return Response({'attends': list_student}, status=200)
        else:
            return Response({'message': 'failed'}, status=401)


# API Get data  And do Face Recognition
from io import BytesIO
import time
import os
import PIL.Image
import dlib
import numpy as np
from face_recognition.api import _raw_face_landmarks

try:
    import face_recognition_models
except Exception:
    print("Please install `face_recognition_models` with this command before using `face_recognition`:\n")
    print("pip install git+https://github.com/ageitgey/face_recognition_models")
    quit()
face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

predictor_5_point_model = face_recognition_models.pose_predictor_five_point_model_location()
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)

cnn_face_detection_model = face_recognition_models.cnn_face_detector_model_location()
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)

face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


def face_encodings(face_image, known_face_locations=None, num_jitters=1):
    """
    Given an image, return the 128-dimension face encoding for each face in the image.

    :param face_image: The image that contains one or more faces
    :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
    :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
    :return: A list of 128-dimensional face encodings (one for each face in the image)
    """
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model="small")
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for
            raw_landmark_set in raw_landmarks]


def get_list_of_list_face_vector_in_class_imgs(in_memory_uploaded_file_data, m_json_data):
    required_size = (160, 160)

    index = 0
    list_of_list_face_in_each_img = []

    for file in in_memory_uploaded_file_data:

        image_data = file.read()
        test_image = Image.open(io.BytesIO(image_data))
        # test_image = ImageOps.exif_transpose(image)

        list_face_vector_in_img = []
        list_face_rect_in_img = m_json_data[index]['face_rect']
        for rect in list_face_rect_in_img:
            x1 = rect['left']
            x2 = rect['right']
            y1 = rect['top']
            y2 = rect['bottom']
            box = (x1, y1, x2, y2)
            # print(box)
            resized_img = test_image.crop(box)
            resized_img = resized_img.resize(required_size, Image.ANTIALIAS)

            temp_file = BytesIO()
            resized_img.save(temp_file, format="jpeg")
            temp_file.name = 'test.jpg'
            temp_file.seek(0)
            restored_img = Image.open(temp_file)
            restored_img = np.array(restored_img)
            try:
                img_vector = face_encodings(restored_img, known_face_locations=[(0, 160, 160, 0)])[0]
            except IndexError:
                img_vector = np.zeros(128)
                pass
            list_face_vector_in_img.append(img_vector)

        list_of_list_face_in_each_img.append(list_face_vector_in_img)
        index += 1

    return list_of_list_face_in_each_img


def preprocess_image(image_path):
    img = load_img(image_path, target_size=(160, 160))
    return np.array(img)


# load images and extract faces for all images in a directory
def load_faces(directory):
    faces = list()
    paths = list()
    list_all_files = sorted(listdir(directory))
    list_img_files = []
    for file in list_all_files:
        if file.endswith('.jpg') or file.endswith('.JPG'):
            list_img_files.append(file)

    for filename in list_img_files:

        path = directory + filename
        fname, _ = os.path.splitext(filename)

        numpy_vector_path = directory + fname
        numpy_ext = ".npy"

        if os.path.isfile(numpy_vector_path + numpy_ext):
            # get pre-caculated vector of face image
            img_vector = np.load(numpy_vector_path + numpy_ext)
        else:
            # get face
            # start_time = time.time()
            img = preprocess_image(path)

            try:
                # (top, right, bottom, left)
                img_vector = face_encodings(img, known_face_locations=[(0, 160, 160, 0)])[0]
                # ---> array [[128-d vector for face 1], [128-d vector for face 2], ....]
                # print("extract 1 img vector--- %s seconds ---" % (time.time() - start_time))
                # save img_vector to use later
                np.save(numpy_vector_path, img_vector)

                if len(paths) == 0:
                    paths.append(path)
            except IndexError:
                pass

        faces.append(img_vector)
    return (faces, paths)


def load_student_trainX_trainY(list_student, STUDENT_IMG_DIR):
    train_X = []
    train_Y = []
    check_paths = []

    for student in list_student:
        student_code = student.student_code
        # print (student_code)
        student_img_folder = STUDENT_IMG_DIR + student_code + "/images/"
        # skip any files that might be in the dir
        if not isdir(student_img_folder):
            continue

        faces_paths = load_faces(student_img_folder)
        labels = [student_code for _ in range(len(faces_paths[0]))]
        # print(len(labels))
        train_X.extend(faces_paths[0])
        train_Y.extend(labels)
        check_paths.extend(faces_paths[1])

    return train_X, train_Y


import json


@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST"])
def schedule_create(request, template_name='schedule_form.html'):
    if request.method == 'POST':
        import time

        start_time = time.time()

        form = ScheduleForms(request.POST or None, request.FILES or None)

        # boundingBox in class room images
        m_json_str = form.data.getlist('json_data')[0]
        m_json_data = json.loads(m_json_str)

        print(m_json_data)

        # class room images
        in_memory_uploaded_file_data = request.FILES.getlist('files')

        # extract all faces in classroom images
        list_of_list_face_vector_in_each_img = get_list_of_list_face_vector_in_class_imgs(in_memory_uploaded_file_data,
                                                                                          m_json_data)
        print(np.shape(list_of_list_face_vector_in_each_img))

        print("get_list_of_list_face_vector_in_class_imgs--- %s seconds ---" % (time.time() - start_time))

        # get all list stutdent in class
        m_schedule_code = form.data.getlist('schedule_code')[0]
        course_id = list(Schedule.objects.filter(schedule_code=m_schedule_code).values('course'))[0]
        list_student = list(Student.objects.filter(course__course_code=course_id['course']))

        student_dict = {}
        for student in list_student:
            student_code = student.student_code
            student_name = student.first_name
            student_dict[student_code] = {'student_code': student_code, 'name': student_name, 'recognized': 0,
                                          'score': 100}

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        STUDENT_IMG_DIR = BASE_DIR + '/media/students/'

        # build vectors for all faces in classroom images
        trainX, trainY = load_student_trainX_trainY(list_student, STUDENT_IMG_DIR)

        print("load_student_trainX_trainY--- %s seconds ---" % (time.time() - start_time))

        NUM_NEIGHBOR = 1
        neigh = NearestNeighbors(n_neighbors=NUM_NEIGHBOR, metric='cosine')
        neigh.fit(trainX)

        # for revert
        train_Y_arr = np.array(trainY)

        COSIN_THREADHOLD = 0.06
        recognition_result = []
        # Threshold see: https://sefiks.com/2018/09/03/face-recognition-with-facenet-in-keras/
        # https://medium.com/beesightsoft/build-your-own-face-recognition-using-face-recognition-library-and-k-nearest-neighbors-classifier-611ffc973d4b
        for face_vector_list in list_of_list_face_vector_in_each_img:
            # face_vector_list: image vectors for faces in each image
            neigh_dist, neigh_ind = neigh.kneighbors(face_vector_list, n_neighbors=NUM_NEIGHBOR)

            # print(neigh_dist)
            # print(neigh_ind)

            recognized_labels = train_Y_arr[neigh_ind].flatten().tolist()
            # filter unrecognized faces if distances surpass threadhold
            for i in range(len(recognized_labels)):
                if (neigh_dist[i] > COSIN_THREADHOLD):
                    recognized_labels[i] = 'unknown'

            scores = neigh_dist.flatten().tolist()
            labels_and_scores = (recognized_labels, scores)
            recognition_result.append(labels_and_scores)

        print(recognition_result)
        for i, image_info in enumerate(m_json_data):
            face_rect = image_info['face_rect']
            response_labels = recognition_result[i][0]
            response_scores = recognition_result[i][1]

            for index, face in enumerate(face_rect):
                detected_student_id = response_labels[index]
                face['student_id'] = response_labels[index]
                face['score'] = response_scores[index]
                detected_student_score = face['score']

                if detected_student_id in student_dict:
                    personal_dict = student_dict[detected_student_id]
                    personal_dict['recognized'] = 1
                    face['name'] = personal_dict['name']
                    if personal_dict['score'] > detected_student_score:
                        personal_dict['score'] = detected_student_score
                else:
                    face['name'] = 'unknown'

        list_student_with_recognition_info = list(student_dict.values())
        list_student_with_recognition_info = sorted(list_student_with_recognition_info, key=lambda i: i['score'])

        json_response = {'list_student': list_student_with_recognition_info,
                         'json_response_for_uploaded_images': m_json_data}

        response_str = json.dumps(json_response)
        print(response_str)
        print("response_str--- %s seconds ---" %
              (time.time() - start_time))
        # save form here
        schedule_code = form.data.get('schedule_code')
        schedule = get_object_or_404(Schedule, schedule_code=schedule_code)
        for each in in_memory_uploaded_file_data:
            ScheduleImagesData.objects.create(image_data=each, schedule=schedule)

        return HttpResponse(response_str, content_type='application/json')

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
