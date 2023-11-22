from django.urls import path
from .views import RegisterAPI, LoginAPI, UserDetailsAPI, LogoutApi#, ForgetPassword,



urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("user_details/", UserDetailsAPI.as_view(), name="user details"),
    # path("forget_password/", ForgetPassword.as_view(), name="forget password"),
    # path("password_reset/<str:token>", LogoutApi.as_view(), name="password reset"),
    path("logout/", LogoutApi.as_view(), name="logout"),
]
