from django.urls import path
from .views import Register, Login, UserDetails, Logout

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('user_details/', UserDetails.as_view(), name='user details'),
    path('logout/', Logout.as_view(), name='logout'),
]