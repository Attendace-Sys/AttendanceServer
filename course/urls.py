from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'schedule'
router = routers.DefaultRouter()
router.register('schedule', views.ScheduleSerializerView)
router.register('images', views.ScheduleImagesDataView)

urlpatterns=router.urls
urlpatterns = [
    path('serializer/', include(router.urls)),
    path('new', views.schedule_create, name='schedule_new'),
    path('edit/<int:schedule_code>/', views.schedule_update, name='schedule_edit'),
]