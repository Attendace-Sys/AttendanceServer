from django.urls import path, include
from User.views import *


urlpatterns = [
    path('user/', UserListViewAPI.as_view())
]