from django.conf.urls import url
from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'User'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^index/$', views.index, name='index'),
    # path('user/', UserListView.as_view())
    # path('<int:id>/details/', user_details, name="user_details"),
    # path('<int:id>/edit/', user_edit, name="user_edit"),
    # path('<int:id>/delete/', user_delete, name="user_delete"),
]