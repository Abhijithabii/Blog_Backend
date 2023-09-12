from django.urls import path
from .views import *

urlpatterns = [
    path('blogs-view/', BlogListView.as_view() , name='lists_of_blogs' ),
    path('blogs-manage/<int:id>/', BlogUpdateRetriveDeleteView.as_view(), name='blogs_management'),
    path('user-related-blogs/<int:id>/', UserRelatedBlogsView.as_view(), name="user_related_blogs"),
    path('comments/<int:id>/', CommentListView.as_view(), name="blog_related_comments"),
    path('create-comment/<int:course_id>/<int:user_id>/', BlogPostCommentsCreateView.as_view(), name='create-comment'),

]