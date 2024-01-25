from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .authentications import CustomAuthentication
from .models import Blogs
from .serializers import BlogSerializer
from users.models import User


class ListBlogs(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def get(self, request):
        try:
            blogs = Blogs.objects.all()
            serializer = BlogSerializer(blogs, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise exceptions.APIException(detail='No blogs found!')
    
    
class ListAuthorBlogs(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            blog = Blogs.objects.filter(author=user.id)
            serializer = BlogSerializer(instance=blog, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise exceptions.APIException(detail='No blogs found!')
    
    
class CreateBlogs(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user)
            return Response(data='Blog created', status=status.HTTP_201_CREATED)
    
        return exceptions.APIException(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class BlogDetails(APIView): # fix patch and delete for author only
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    def get(self, request, pk):
        try:
            blog = Blogs.objects.get(id=pk)
            serializer = BlogSerializer(blog)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise exceptions.APIException(detail='No blogs found!')
        
    def patch(self, request, pk):
        user = User.objects.get(id=request.user.id)
        blog = Blogs.objects.get(id=pk)
        data = request.data
        serializer = BlogSerializer(data=data, instance=blog, partial=True)
        if user.id == blog.author_id:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data='Blog updated', status=status.HTTP_200_OK)
            return exceptions.APIException(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise exceptions.AuthenticationFailed(detail='Only the author is allowed to update this blog')
    
    def delete(self, request, pk):
        user = User.objects.get(id=request.user.id)
        blog = Blogs.objects.get(id=pk)
        if user.id == blog.author_id:
            blog.delete()
            return Response(data='Blog deleted', status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.AuthenticationFailed(detail='Only the author is allowed to delete this blog')
    
    
class Test(APIView):
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def get(self, request):
        blog = Blogs.objects.get(id=3)
        author = blog.author_id
        serializer = BlogSerializer(instance=author)
        return Response(data=serializer.data)
        