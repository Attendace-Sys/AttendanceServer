"""DjangoAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url, include
from User import views

# from User.views import (LoginView, LogoutView)

admin.site.site_header = 'Trang Web Admin'
admin.site.site_title = 'Django Admin page'
admin.site.index_title = 'Django Admin page'

router = routers.DefaultRouter()
urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  path('admin/', admin.site.urls, name='admin'),
                  path('teachers/', include('teacher.urls')),
                  path('students/', include('student.urls')),
                  path('courses/', include('course.urls')),
                  path('user/', include('User.urls')),
                  path('api/v1/', include('course.api_urls')),
                  path('api/v1/', include('student.api_urls')),
                  path('api/v1/', include('teacher.api_urls')),
                  path('api/v1/', include('User.api_urls')),
                  path('api/v1/auth/login/', views.LoginView.as_view()),
                  path('api/v1/auth/logout/', views.LogoutView.as_view()),
                  # path('users/', include('django.contrib.auth.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
