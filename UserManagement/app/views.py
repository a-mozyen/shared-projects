from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .services import create_token, user_identefier, get_user
from .authentications import CustomAuthentication
from django.contrib.auth.hashers import check_password, make_password
from .models import User


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
        
        # retrieve user data from database 
        user = user_identefier(email=email)
        
        if user is None:
            raise exceptions.AuthenticationFailed("Wroge credentials")
        
        # check if the entered password is what stored in database 
        pwd = check_password(password=password, encoded=user.password)
        
        if not pwd or None:
            raise exceptions.AuthenticationFailed("Wrong credentials")

        # create token with the given details
        token = create_token(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email)

        resp = Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserDetailsAPI(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        # get the token from the request, decode it and check if it's valid
        user = get_user(request=request)

        return Response(user, status=status.HTTP_200_OK)
    
class UserUpdate(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        user = get_user(request=request)
        
        return Response(user, status=status.HTTP_200_OK)
    
    #This methode update user information
    def put(self, request):
        user = get_user(request=request)
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.update(user, serializer)
        
        return Response(serializer.data , status=status.HTTP_200_OK)
        # serializer = UserSerializer(user, data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutApi(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.data
        resp = Response(user)
        resp.delete_cookie("jwt")
        resp.data = {"Logout Successful"}
        return resp
        