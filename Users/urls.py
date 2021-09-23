from django.urls import include, path

from .views import UsersPostGet, UserGetPutDelete, UsersLogin

urlpatterns = [
    path('', UsersPostGet.as_view()),
    path('<int:pk>/', UserGetPutDelete.as_view()),
    path('login/', UsersLogin.as_view()),
]
