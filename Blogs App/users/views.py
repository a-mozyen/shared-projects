from rest_framework.views import APIView
from rest_framework import exceptions, status, permissions
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer
from .authentications import create_token, CustomAuthentication
from .models import User


class Register(APIView):
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()

        return Response(data='User created', status=status.HTTP_201_CREATED)
    
class Login(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            user = User.objects.get(username=username)
        except:
            raise exceptions.APIException('User not found')
        
        try:
            password = request.data.get('password')
            check_password(password=password, encoded=user.password)
        except:
            raise exceptions.AuthenticationFailed('Wrong password')
        
        user.update_last_login()
        token = create_token(id=user.id, email=user.email, username=user.username)
        response = Response(data='Login successfull', status=status.HTTP_200_OK)
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        return response
    

class UserDetails(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(id=request.user.id)
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data='User updated')
        
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        response = Response(data='User deleted', status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('jwt')

        return response

class logout(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]
    
    def post(self, request):
        response = Response(data='Logout successfull', status=status.HTTP_200_OK)
        response.delete_cookie('jwt')

        return response
