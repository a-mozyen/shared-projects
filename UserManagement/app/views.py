from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .services import create_token, user_identefier
from .authentications import CustomAuthentication
from django.conf import settings
import jwt


class RegisterAPI(APIView):
    def post(self, request):
        # creates an instance of the UserSerializer and initializes it with the data from the HTTP POST request
        user = UserSerializer(data=request.data) 
        if user.is_valid(raise_exception=True): # check if the data is valid or raise an exception
            user.save()
        # return the responce where the data is the data from user variable
        return Response(data=user.data, status=status.HTTP_201_CREATED)

    
class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = user_identefier(email=email)
        
        if user is None:
            raise exceptions.AuthenticationFailed("Wroge email")

        if password != user.password:    #not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Wrong password")

        token = create_token(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email)

        resp = Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserDetailsAPI(APIView):
    authentication_classes = [CustomAuthentication,]
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise exceptions.AuthenticationFailed('Permission denied, Login to access this page.')
        
        try:
            user = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except:
            raise exceptions.AuthenticationFailed('Permission denied')

        return Response(user, status=status.HTTP_200_OK)


class LogoutApi(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.data
        resp = Response(user)
        resp.delete_cookie("jwt")
        resp.data = {"message": "Logout Successful"}
        return resp
    