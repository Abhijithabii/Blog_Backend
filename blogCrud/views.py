from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from blogApp.models import *
from .serializers import *
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

# Create your views here.

class BlogListView(APIView):

    parser_classes = [MultiPartParser]

    def get(self, request):
        blogs = BlogPosts.objects.all()
        serializer = BlogPostsSerializer(blogs, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        serializer = BlogPostsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        


class BlogUpdateRetriveDeleteView(APIView):
    parser_classes = [MultiPartParser]

    def get_blog(self, id):
        try:
            return BlogPosts.objects.get(id=id)
        except BlogPosts.DoesNotExist:
            raise Http404

    def get(self, request, id):
        blog = self.get_blog(id)
        serializer = BlogPostsSerializer(blog)
        return Response(serializer.data)
    
    def put(self, request, id):
        blog = self.get_blog(id)
        serializer = BlogPostsSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        blog = self.get_blog(id)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserRelatedBlogsView(APIView):
    
    def get(self, request, id):
        author = CustomUser.objects.get(id=id)
        blogs = BlogPosts.objects.filter(author=author)
        serializer = BlogPostsSerializer(blogs, many=True)
        return Response(serializer.data)




class CommentListView(APIView):
    def get_blog(self, id):
        try:
            return BlogPosts.objects.get(id=id)
        except BlogPosts.DoesNotExist:
            raise Http404
    def get(self, request , id):
        blog_posts = self.get_blog(id)
        comments = BlogPostComments.objects.filter(post=blog_posts)
        serializer = CommentViewSerializer(comments, many=True)
        return Response(serializer.data)
    

class BlogPostCommentsCreateView(APIView):
    def post(self, request, course_id, user_id):
        try:
            course = BlogPosts.objects.get(pk=course_id)
            user = CustomUser.objects.get(pk=user_id)
            data = {
                'author_id': user.id,
                'post_id': course.id,
                'content': request.data.get('content')
            }
            serializer = CreateCommentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except (BlogPosts.DoesNotExist, CustomUser.DoesNotExist):
            return Response({'error': 'Course or user not found.'}, status=status.HTTP_404_NOT_FOUND)