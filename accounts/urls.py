from django.urls import path
from .views import *
from .rest_views import *
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm

app_name = "accounts"
urlpatterns = [
    path('login/', LoginFormView.as_view(), name="login_form"),
    path('logout/', LogOut.as_view(),name='logout'),
    path('signup/', SignUpFormView.as_view(), name="Signup_form"),
    path('profile/', view_profile, name="view_profile"),
    path('followers/<int:pk>', FollowersList, name="followers_list"),
    path('following/<int:pk>', FollowingsList, name="followings_list"),
    path('profile/update/<int:pk>', UserProfileUpdate.as_view(), name="update_profile"),
    path('users/', UserListView.as_view(), name="user_list"),
    path('users/<int:pk>', UserDetailView.as_view(), name="user_detail"),
    path('users/<int:id>/follow', FollowToggle.as_view(), name="follow_toggle"),
    path('reset-password/', password_reset, name="password_reset"),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    path('reset-password/confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('users/api/<slug:slug>', SearchApi.as_view(), name="search_api"),
]