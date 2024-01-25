from django.urls import path
from .views import ListBlogs, ListAuthorBlogs, CreateBlogs, BlogDetails, Test


urlpatterns = [
    path('list_blogs/', ListBlogs.as_view(), name='list blogs'),
    path('list_author_blogs/', ListAuthorBlogs.as_view(), name='list author blogs'),
    path('create_blog/', CreateBlogs.as_view(), name='create blog'),
    path('blog_details/<int:pk>/', BlogDetails.as_view(), name='blog details'),
    path('test/', Test.as_view(), name='test')
]