from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf.urls import url
from . import views

app_name = 'student'
router = routers.DefaultRouter()
router.register('students', views.StudentSerializerView)
router.register('images', views.StudentImagesDataView)

urlpatterns=router.urls
urlpatterns = [
    path('serializer/', include(router.urls)),
    path('list', views.student_list, name='student_list'),
    path('new', views.student_create, name='student_new'),
    path('edit/<int:student_code>', views.student_update, name='student_edit'),
    path('delete/<int:student_code>', views.student_delete, name='student_delete'),
]
