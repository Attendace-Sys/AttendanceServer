from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('students', views.StudentView)
router.register('images', views.StudentImagesDataView)
urlpatterns = [
    path('', include(router.urls)),
]