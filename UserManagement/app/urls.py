from django.urls import path
from .views import RegisterAPI, LoginAPI, UserDetailsAPI, LogoutApi, UserUpdate 


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('user_details/', UserDetailsAPI.as_view(), name='user details'),
    path('user_update/', UserUpdate.as_view(), name='user update'),
    path('logout/', LogoutApi.as_view(), name='logout'),
]
