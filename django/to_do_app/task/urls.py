from django.urls                import path,include

from .views                     import (
    UserLoginView,
    TaskListView,
    RegisterView,
    UserListView,
)

from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'tasks',TaskListView)

app_name = 'task'

urlpatterns = [
    path('login/',          UserLoginView.as_view()),
    path('tasks/',          TaskListView.as_view()),
    # path('tasks/<int:id>',  TaskListView.as_view()),
    path('register/',       RegisterView.as_view()),
    path('users/',          UserListView.as_view()),
    # path('',                include(router.urls)),
    # path('logout/', LogoutView.as_view()),
]