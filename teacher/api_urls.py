from django.urls import path, include
from teacher.views import *


urlpatterns = [
    path('teacher/', TeacherListViewAPI.as_view())
]