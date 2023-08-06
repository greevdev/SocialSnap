from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from SocialSnap.app_auth.models import User
from .forms import EditProfileForm
from.models import Profile, Post


def landing_page(request):
    return render(request, template_name='common/landing.html')


@login_required
def dashboard_page(request):
    context = {
        'username': request.user.get_username()
    }

    return render(request, context=context, template_name='common/dashboard.html')


class UserProfileView(View, LoginRequiredMixin):
    template_name = 'common/profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)

        posts = Post.objects.filter(creator=user)
        post_count = posts.count()
        followers_count = profile.followers.count()
        following_count = profile.following.count()

        is_following = request.user.is_authenticated and profile.followers.filter(pk=request.user.pk).exists()

        context = {
            'user': user,
            'profile': profile,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': profile.bio,
            'profile_pic': profile.profile_picture,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'post_count': post_count,
            'is_following': is_following,
        }

        return render(request, self.template_name, context=context)


@login_required
def my_profile(request):
    username = request.user.username

    url = reverse('user profile', kwargs={'username': username})

    return redirect(url)


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_follow_profile = get_object_or_404(Profile, user__username=username)
        logged_in_user_profile = request.user.profile

        # Check if the logged-in user is already following the user_to_follow
        if user_to_follow_profile in logged_in_user_profile.following.all():
            # If already following, redirect back to the user profile
            return redirect('user profile', username=username)
        else:
            # If not already following, add the follow relationship
            user_to_follow_profile.followers.add(logged_in_user_profile)
            logged_in_user_profile.following.add(user_to_follow_profile)
            return redirect('user profile', username=username)


class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_unfollow_profile = get_object_or_404(Profile, user__username=username)
        logged_in_user_profile = request.user.profile

        # Check if the logged-in user is following the user_to_unfollow
        if user_to_unfollow_profile in logged_in_user_profile.following_profiles.all():
            # If following, remove the follow relationship
            logged_in_user_profile.following_profiles.remove(user_to_unfollow_profile)
            user_to_unfollow_profile.followers_profiles.remove(logged_in_user_profile)

        return redirect('user profile', username=username)


@login_required
def search_view(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        try:
            profile = get_object_or_404(Profile, user__username=query)
            return redirect('user profile', username=profile.user.username)
        except Profile.DoesNotExist:
            raise Http404("User not found")
    else:
        return redirect('dashboard page')


@login_required
def settings_view(request):
    context = {
        'username': request.user.get_username()
    }

    return render(request, context=context, template_name='common/settings.html')


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'common/edit-profile.html'

    def get(self, request, username):
        user = request.user
        profile = Profile.objects.get(user=user)
        form = EditProfileForm(initial={
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email': profile.user.email,
            'bio': profile.bio,
        })
        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, username):
        user = request.user
        profile = Profile.objects.get(user=user)
        form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('user profile', username=user.username)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)


def custom_404(request, exception):
    return render(request, 'common/404.html', status=404)
