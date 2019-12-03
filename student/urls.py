from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf.urls import url

router = routers.DefaultRouter()
router.register('students', views.StudentSerializerView, basename='serializers')
router.register('images', views.StudentImagesDataView, basename='images')

urlpatterns=router.urls


urlpatterns = [
    path('serializer', include(router.urls)),
    url(r'^$', views.StudentView.as_view()),
]
