from django.urls import path
from .views import *
from .rest_views import *
app_name = "posts"

urlpatterns = [
    path('', NewsFeed.as_view(),name="news_feed"),
    path('<int:pk>', PostDetailView.as_view(), name="post_details"),
    path('<int:pk>/likes', LikesList, name="post_likes"),
    path('<int:pk>/comment', addComment, name="post_add_comment"),
    path('add/', AddPost.as_view(), name="add_post"),
    path('edit/<int:pk>', EditPost.as_view(), name="edit_post"),
    path('delete/<int:pk>', DeletePost.as_view(), name="delete_post"),
    path('likes/api/', LikesListApi.as_view(), name="user_likes_api"),
    path('like/<int:post_id>', LikesToggle.as_view(), name="like_toggle"),
]