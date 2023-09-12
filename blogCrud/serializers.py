from rest_framework import serializers
from blogApp.models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id', 'username', 'email']



class BlogPostsSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    class Meta:
        model = BlogPosts
        fields = ['id', 'author', 'title', 'blog_image', 'content']



class BlogPostsCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    class Meta:
        model = BlogPosts
        fields = ['id', 'author_id', 'title', 'blog_image', 'content']

    def validate_author_id(self, value):
        try:
            author = CustomUser.objects.get(pk=value.pk)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid author ID.")
        return author.id


class CommentViewSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    post = BlogPostsSerializer()
    class Meta:
        model = BlogPostComments
        fields = ['id', 'author', 'post', 'content']

class CreateCommentSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=BlogPosts.objects.all(), write_only=True)
    class Meta:
        model = BlogPostComments
        fields = ['id', 'author_id', 'post_id', 'content']

    def validate_author_id(self, value):
        try:
            author = CustomUser.objects.get(pk=value.pk)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid author ID.")
        return author.id
    
    def validate_post_id(self, value):
        try:
            post = BlogPosts.objects.get(pk=value.pk)
        except BlogPosts.DoesNotExist:
            raise serializers.ValidationError("Invalid post ID.")
        return post.id 



    

