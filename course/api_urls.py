from django.urls import path, include
from course.views import *
from student.views import StudentAttendanceOfACourse


urlpatterns = [
    path('course/', CourseListViewAPI.as_view()),
    path('course/<str:course_code>/', CourseListViewAPI.as_view()),
    path('courses/teacher/', CourseListViewByTeacherAPI.as_view()),
    # api get list course of teacher
    path('courses/teacher/<str:teacher>/', CourseListViewByTeacherAPI.as_view()),
    path('schedule/', ScheduleListViewAPI.as_view()),
    path('schedule/<str:schedule_code>/', ScheduleListViewAPI.as_view()),
    path('schedules/course/', ScheduleListViewByCourseAPI.as_view()),
    # api get list schedule of course
    path('schedules/course/<str:course>/', ScheduleListViewByCourseAPI.as_view()),
    path('schedules/image/', ScheduleImagesDataListViewByScheduleAPI.as_view()),
    path('schedules/image/<str:schedule>/', ScheduleImagesDataListViewByScheduleAPI.as_view()),
    path('attendance/', AttendanceListViewAPI.as_view()),
    path('attendance/<str:attendance_code>/', AttendanceListViewAPI.as_view()),
#     path('attendances/student/', AttendanceListViewByStudentAPI.as_view()),
#     path('attendances/student/<str:student>/', AttendanceListViewByStudentAPI.as_view()),
    path('attendances/schedule/', AttendanceListViewByScheduleAPI.as_view()),
    # api get list attendance of schedule
    path('attendances/schedule/<str:schedule_code>/', AttendanceListViewByScheduleAPI.as_view()),
    # api upload list student (absent status, attendance code)
    path('updatelist/', UpdateListAttendancesViewAPI.as_view()),
    # api upload - get data attendance from mobile app
    path('upload_checking_attendance/', UploadCheckingAttendanceViewAPI.as_view()),
    # api get all schedule code and attendance status of a course of student
    path('student/schedule_attendance_status/<str:course_code>/<str:student_code>', StudentAttendanceOfACourse.as_view()),

]
