from django.urls import path, include
from student.views import *


urlpatterns = [
    path('student/', StudentListViewAPI.as_view()),
    path('student/<str:student_code>/', StudentListViewByStudentAPI.as_view()),
    path('students/images/', StudentImagesDataListViewAPI.as_view()),
    path('students/images/<str:student>/', StudentImagesDataListViewByStudentAPI.as_view()),
    path('students/list_course/<str:student>/', StudentGetListCourseByStudentAPI.as_view()),
    # api get all schedule code and attendance status of a course of student
    path('student/schedule_attendance_status/<str:course_code>/<str:student_code>/', StudentAttendanceOfACourse.as_view()),

]