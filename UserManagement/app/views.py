from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .services import create_token
from .authentications import CustomAuthentication
from django.contrib.auth.hashers import check_password
from .models import User
from django.core.mail import send_mail


class RegisterAPI(APIView):
    def post(self, request):
        # creates an instance of the UserSerializer and initializes it with the data from the HTTP POST request
        user = UserSerializer(data=request.data)  # wrapper object

        if user.is_valid(raise_exception=True):  # check if the data is valid or raise an exception
            user.save()
            # return the responce where the data is the data from user variable
            return Response(data="User created successfully", status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self, request):
        try:
            # get the email and password from the request sent by user
            email = request.data.get("email")
            email = email.lower()
            password = request.data.get("password")
            # retrieve user data from database
            user = User.objects.get(email=email)

        except:
            raise exceptions.AuthenticationFailed('User not found!')

        if not user:
            raise exceptions.AuthenticationFailed(detail="Wroge credentials")
        # check if the entered password is what stored in database
        pwd = check_password(password=password, encoded=user.password)
        if not pwd:
            raise exceptions.AuthenticationFailed(detail="Wrong credentials")
        
        user.update_last_login()
        # create token with the given details
        token = create_token(id=user.id, email=user.email)

        responce = Response(data="Login successfull", status=status.HTTP_200_OK)
        responce.set_cookie(key="jwt", value=token, httponly=True)
        return responce


# class ForgetPassword(APIView):  # NOT finished (under devlopement)
#     def post(self, request, email):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data["email"]
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response(data="User not found", status=status.HTTP_404_NOT_FOUND)

#             # Generate a token and send it to the user's email for verification
#             # In a real-world scenario, you might want to use a library like Django Rest Framework's TokenAuthentication or JWT for more secure token handling.
#             # For simplicity, we'll just include the user's ID in the email link as a basic example.
#             reset_token = str(user.id)
#             reset_link = f"http://localhost:8000/password_reset/{reset_token}/"

#             # Send the reset link to the user's email
#             send_mail(
#                 "Password Reset",
#                 f"Click the following link to reset your password: {reset_link}",
#                 "from@example.com",
#                 [email],
#                 fail_silently=False)

#             return Response(data="Password reset email sent successfully", status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsAPI(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # This methode update user information
    def patch(self, request):
        user = User.objects.get(id=request.user.id)
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(data="Updated Successfully", status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()

        response = Response(data='User deleted successfully', status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('jwt')
        return response


class LogoutApi(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        responce = Response(status=status.HTTP_200_OK)
        responce.delete_cookie("jwt")
        responce.data = {"Logout Successful"}
        return responce


class Test(APIView):  # for testing only
    pass 
