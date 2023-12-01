from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .authentications import CustomAuthentication, create_token
from .serializers import UserSerializer
from .models import User


class Register(APIView):
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()
            return Response(data='User created', status=status.HTTP_201_CREATED)
        else:
            raise APIException(detail=user.errors)


class Login(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            email = email.lower()
            user = User.objects.get(email=email)
        except:
            raise APIException(detail='Wrong credentials')
        
        try:
            password = request.data.get('password')
            check_password(password=password, encoded=user.password)
        except:
            raise APIException(detail='Wrong credentials')
        
        token = create_token(id=user.id, username=user.username, email=user.email)
        responce = Response(data="Login successfull", status=status.HTTP_200_OK)
        responce.set_cookie(key="jwt", value=token, httponly=True)
        return responce


class UserDetails(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(id=request.user.id)
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data="Successfully updated", status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        response = Response(data='User deleted', status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('jwt')
        return response

class Logout(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        responce = Response(data='Logout Successfull' , status=status.HTTP_200_OK)
        responce.delete_cookie("jwt")
        return responce
