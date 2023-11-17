from django.urls import path
from .views import RegisterAPI, LoginAPI, UserDetailsAPI, LogoutApi


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('user_details/', UserDetailsAPI.as_view(), name='user details'),
    path('logout/', LogoutApi.as_view(), name='logout'),
]