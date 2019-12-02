from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('courses', views.TeacherView)
urlpatterns = [
    path('', include(router.urls)),
]