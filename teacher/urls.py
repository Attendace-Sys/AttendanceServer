from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'teacher'
router = routers.DefaultRouter()
router.register('teacher', views.TeacherView)
urlpatterns = [
    path('teacher/', include(router.urls)),
    path('list', views.teacher_list, name='teacher_list'),
    path('new', views.teacher_create, name='teacher_new'),
    path('edit/<int:teacher_code>', views.teacher_update, name='teacher_edit'),
    path('delete/<int:teacher_code>', views.teacher_delete, name='teacher_delete'),
    ]