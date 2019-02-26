from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.exceptions import PermissionDenied

from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from posts.models import *
# Create your views here.


class UserListView(LoginRequiredMixin,ListView):
    login_url = "accounts/login/"
    model = UserProfile
    context_object_name = 'data'
    template_name = 'accounts/users_list.html'

    def get_queryset(self):
        return UserProfile.objects.filter(~Q(user=self.request.user))


@login_required(login_url='/accounts/login/')
def FollowersList(request, **kwargs):
    user = User.objects.get(id=kwargs['pk'])
    args = {
        'data': Follow.objects.filter(following=user),
        'title': "Followers"
    }
    return render(request, 'accounts/followers.html', args)


@login_required(login_url='/accounts/login/')
def FollowingsList(request, **kwargs):
    user = User.objects.get(id=kwargs['pk'])
    args = {
        'data': Follow.objects.filter(follower=user),
        'title': "Following"
    }
    return render(request, 'accounts/followings.html', args)


class UserDetailView(LoginRequiredMixin,DetailView):
    login_url = "/accounts/login/"
    model = UserProfile

    def get_context_data(self, **kwargs):

        context = super(UserDetailView,self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        followers = Follow.objects.filter(following=profile.user).count()
        following = Follow.objects.filter(follower=profile.user).count()
        isFollowing = Follow.objects.filter(follower=self.request.user,following=profile.user ).count()
        posts = Posts.objects.filter(uploader=profile.user)
        context.update({
            'followers': followers,
            'following': following,
            'profile': profile,
            'isFollowing': isFollowing,
            'posts':posts
        })
        return context


class FollowToggle(View):

    def get(self,*args,**kwargs):
        follower = self.request.user
        following = User.objects.get(id=self.kwargs.get('id'))
        following_obj = Follow.objects.filter(following=following,follower=follower)
        response = 0
        if following_obj.count():
            following_obj.delete()

        else:
            Follow.objects.create(follower=follower,following=following)
            response = 1

        return HttpResponse(response)


class LoginFormView(PermissionRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(
            request,
            template_name='accounts/login_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:

                login(request,user)
                return redirect('posts:news_feed')
            else:
                return redirect('accounts:Signup_form')
        else:
            form = LoginForm(request.POST)
            return render(
                request,
                template_name='accounts/login_form.html',
                context={
                    'form': form,
                    'errors': form.errors
                }
            )

    def has_permission(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('posts:news_feed')


class SignUpFormView(PermissionRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(
            request,
            template_name='accounts/signup_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:

                login(request,user)
                return redirect('accounts:update_profile', pk=user.id)
            else:
                return redirect('accounts:SignUpform')
        else:
            return render(
                request,
                template_name='accounts/signup_form.html',
                context={
                    'form': form,
                    'errors':form.errors
                }
            )

    def has_permission(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('posts:news_feed')

@login_required(login_url='/accounts/login/')
def view_profile(request):
    user = UserProfile.objects.get(user=request.user)
    followers = Follow.objects.filter(following=request.user).count()
    following = Follow.objects.filter(follower=request.user).count()
    posts = Posts.objects.filter(uploader=request.user)
    args = {
        'userProfile': user,
        'followers': followers,
        'following': following,
        'posts': posts
        }
    return render(request,'accounts/profile.html',args)


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login_form')


class UserProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    login_url = '/accounts/login/'
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/add_user_profile.html'
    success_url = reverse_lazy('accounts:view_profile')

    def has_permission(self):
        user_id = self.kwargs['pk']
        user_details = UserProfile.objects.get(id=user_id)
        return user_details.user == self.request.user

