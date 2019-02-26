from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from rest_framework.exceptions import PermissionDenied

from .forms import *
from accounts.models import *
from .models import *

# Create your views here.


class NewsFeed(LoginRequiredMixin, ListView):
    login_url = "/accounts/login/"
    model = Posts
    context_object_name = 'feeds'
    template_name = 'posts/feeds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follower_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id')
        feeds = Posts.objects.filter(Q(uploader_id__in=follower_ids) | Q(uploader=self.request.user)).order_by('-date_updated')
        feedData = []

        for feed in feeds:
            likes_count = Likes.objects.filter(Liked_post=feed).count()
            feedData.append({'feed': feed, 'likesCount': likes_count})

        liked_posts = Likes.objects.filter(liked_by=self.request.user).values_list('Liked_post_id')
        liked_posts = [value[0] for value in liked_posts]

        context.update({
            'liked_posts': liked_posts,
            'feedsData': feedData,
        })
        return context


class EditPost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Posts
    form_class = PostForm
    template_name = "posts/create_post.html"
    success_url = reverse_lazy('accounts:view_profile')

    def has_permission(self):
        post_id = self.kwargs['pk']
        post_details = Posts.objects.get(id = post_id)
        return post_details.uploader == self.request.user

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect(self.request.META.get("HTTP_REFERER"))


class DeletePost(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Posts
    template_name = "posts/confirm.html"
    success_url = reverse_lazy("accounts:view_profile")

    def has_permission(self):
        post_id = self.kwargs['pk']
        post_details = Posts.objects.get(id = post_id)
        return post_details.uploader == self.request.user

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect(self.request.META.get("HTTP_REFERER"))


@login_required(login_url='/accounts/login/')
def LikesList(request, **kwargs):
    post = Posts.objects.get(id=kwargs['pk'])
    args = {
        'data': Likes.objects.filter(Liked_post=post),
        'title': "Likes"
    }
    return render(request, 'posts/likes.html', args)




class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login'
    model = Posts
    template_name = "posts/post_details.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Posts, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Posts.objects.get(id=self.kwargs['pk'])
        likes = Likes.objects.filter(Liked_post=post)
        comments = Comments.objects.filter(commented_post=post)
        hasLiked = 1 if Likes.objects.filter(Liked_post=post,liked_by=self.request.user) else 0
        user = UserProfile.objects.get(user=post.uploader)
        context.update({
            'post':post,
            'likes': likes,
            'comments': comments,
            'hasLiked': hasLiked,
            'profile': user,
        })
        return context


class AddPost(LoginRequiredMixin, CreateView):
    login_url = 'accounts/login/'
    model = Posts
    form_class = PostForm
    template_name = "posts/create_post.html"

    def post(self, request, *args, **kwargs):
        post = PostForm(request.POST,request.FILES)
        if post.is_valid():
            post = post.save(commit=False)
            post.uploader = request.user
            post.save()
            return redirect('accounts:view_profile')
        else:
            return redirect("posts:add_post")


@csrf_exempt
def addComment(request,**kwargs):
    if request.method == "POST":
        post = Posts.objects.get(id=kwargs['pk'])
        comment = Comments.objects.create(
            commented_post=post,
            comment=request.POST["comment"],
            commented_by=request.user
        )
    response = str(request.user.username)+":"+request.POST["comment"]
    return HttpResponse(response)


class LikesToggle( View):
    def get(self,*args,**kwargs):
        post = Posts.objects.get(id=self.kwargs.get('post_id'))
        user = self.request.user
        like_obj = Likes.objects.filter(liked_by=user,Liked_post=post)
        response = 0

        if like_obj.count():
            like_obj.delete()
        else:
            Likes.objects.create(liked_by=user,Liked_post=post)
            response = 1
        likes_count = Likes.objects.filter(Liked_post=post).count()
        response = str(response)+","+str(likes_count)

        return HttpResponse(response)



