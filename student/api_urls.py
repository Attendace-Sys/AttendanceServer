from django.urls import path, include
from student.views import *


urlpatterns = [
    path('student/', StudentListViewAPI.as_view()),
    path('student/<str:student_code>', StudentListViewByStudentAPI.as_view()),
    path('students/images/', StudentImagesDataListViewAPI.as_view()),
    path('students/images/<str:student>', StudentImagesDataListViewByStudentAPI.as_view()),
]