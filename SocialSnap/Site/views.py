from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from SocialSnap.app_auth.models import User
from .forms import EditProfileForm, DeleteAccountForm, ChangePasswordForm, PostForm, EditPostForm, CommentForm, \
    EditCommentForm
from .models import Profile, Post, Comment


def landing_page(request):
    return render(request, template_name='common/landing.html')


def about_page(request):
    return render(request, template_name='common/about.html')


@login_required
def home_page(request):
    following_profiles = request.user.profile.following_profiles.all()
    posts = Post.objects.filter(creator__profile__in=following_profiles).order_by('-created_at')

    context = {
        'posts': posts,
        'username': request.user.username,
    }

    return render(request, 'common/home.html', context=context)


class UserProfileView(View, LoginRequiredMixin):
    template_name = 'common/profile.html'

    def get(self, request, username):
        try:
            user = get_object_or_404(User, username=username)
            profile = get_object_or_404(Profile, user=user)

            posts = Post.objects.filter(creator=user).order_by('-created_at')
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

        except Exception as e:
            return render(request, 'errors/error.html', {'error_message': str(e)})


@login_required
def my_profile(request):
    username = request.user.username

    url = reverse('user profile', kwargs={'username': username})

    return redirect(url)


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        try:
            user_to_follow_profile = get_object_or_404(Profile, user__username=username)
            logged_in_user_profile = request.user.profile

            if user_to_follow_profile in logged_in_user_profile.following.all():

                return redirect('user profile', username=username)
            else:
                user_to_follow_profile.followers.add(logged_in_user_profile)
                logged_in_user_profile.following.add(user_to_follow_profile)
                return redirect('user profile', username=username)

        except Exception as e:
            return render(request, 'errors/error.html', {'error_message': str(e)})


class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        try:
            user_to_unfollow_profile = get_object_or_404(Profile, user__username=username)
            logged_in_user_profile = request.user.profile

            if user_to_unfollow_profile in logged_in_user_profile.following_profiles.all():
                logged_in_user_profile.following_profiles.remove(user_to_unfollow_profile)
                user_to_unfollow_profile.followers_profiles.remove(logged_in_user_profile)

            return redirect('user profile', username=username)

        except Exception as e:
            return render(request, 'errors/error.html', {'error_message': str(e)})

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
    try:
        user = request.user
        context = {
            'username': user.get_username(),
            'user': user
        }

        return render(request, context=context, template_name='common/settings.html')

    except Exception as e:
        return render(request, 'errors/error.html', {'error_message': str(e)})


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'common/edit-profile.html'

    def get(self, request, username):
        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            form = EditProfileForm(initial={
                'first_name': profile.user.first_name,
                'last_name': profile.user.last_name,
                'email': profile.user.email,
                'bio': profile.bio,
                'profile_picture': profile.profile_picture,
            })
            context = {
                'form': form,
                'user': user
            }
            return render(request, self.template_name, context=context)

        except Exception as e:
            return render(request, 'errors/error.html', {'error_message': str(e)})

    def post(self, request, username):
        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            form = EditProfileForm(request.POST, request.FILES, instance=profile)

            if form.is_valid():
                form.save()
                return redirect('user profile', username=user.username)

            context = {
                'form': form,
                'user': user
            }

            return render(request, self.template_name, context=context)

        except Exception as e:
            return render(request, 'errors/error.html', {'error_message': str(e)})

@login_required
def delete_account(request, username):
    try:
        user = request.user

        if request.method == 'POST':
            form = DeleteAccountForm(request.POST)

            if form.is_valid():
                user = request.user
                password = form.cleaned_data['password']

                if authenticate(request, username=user.username, password=password):
                    user.delete()
                    logout(request)
                    return redirect('landing page')
                else:
                    form.add_error('password', 'Invalid password. Please try again.')

        else:
            form = DeleteAccountForm()

        return render(request, 'common/delete-profile.html', {'form': form, 'user': user})

    except Exception as e:
        return render(request, 'errors/error.html', {'error_message': str(e)})


@login_required()
def change_password(request, username):
    try:
        user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)

            if form.is_valid():
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password1']

                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    return redirect('home page')
                else:
                    form.add_error('current_password', 'Invalid password. Please try again.')

        else:
            form = ChangePasswordForm()

        return render(request, 'common/change-password.html', {'form': form, 'user': user})

    except Exception as e:
        return render(request, 'errors/error.html', {'error_message': str(e)})


@login_required()
def create_post(request, username):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            return redirect('my profile')
    else:
        form = PostForm()

    return render(request, 'common/create-post.html', {'form': form})


class LikePostView(View):
    @method_decorator(login_required)
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})


class EditPostView(LoginRequiredMixin, View):
    template_name = 'common/edit-post.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, creator=request.user)
        form = EditPostForm(instance=post)

        context = {
            'form': form,
            'post': post,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, creator=request.user)
        form = EditPostForm(request.POST, request.FILES, instance=post)

        clear_image = request.POST.get('clear_image')

        if form.is_valid():
            if clear_image:
                post.image.delete(save=False)
            form.save()
            return redirect('user profile', username=request.user.username)

        context = {
            'form': form,
            'post': post,
        }

        return render(request, self.template_name, context=context)


class DeletePostView(LoginRequiredMixin, View):
    template_name = 'common/delete-post.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, creator=request.user)
        context = {
            'post': post,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, creator=request.user)
        post.delete()
        return redirect('user profile', username=request.user.username)


class UserConnectionsView(LoginRequiredMixin, View):
    template_name = 'common/connections.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)

        followers = profile.followers.all()
        following = profile.following.all()

        followers_count = followers.count()
        following_count = following.count()

        context = {
            'user': user,
            'profile': profile,
            'followers': followers,
            'following': following,
            'followers_count': followers_count,
            'following_count': following_count,
        }

        return render(request, self.template_name, context=context)


def custom_404(request, exception):
    return render(request, 'common/../../templates/errors/404.html', status=404)


def custom_500(request, exception):
    return render(request, 'common/../../templates/errors/500.html', status=500)


class ViewPostView(View, LoginRequiredMixin):
    template_name = 'common/view-post.html'

    def get(self, request, post_id):
        try:
            user = request.user
            profile = get_object_or_404(Profile, user=user)

            post = get_object_or_404(Post, id=post_id)

            creator = post.creator
            creator_profile = creator.profile

            comments = post.comments.all().order_by('-created_at')
            context = {
                'user': user,
                'profile': profile,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_pic': profile.profile_picture,
                'creator': creator,
                'creator_profile': creator_profile,
                'creator_username': creator.username,
                'creator_first_name': creator.first_name,
                'creator_last_name': creator.last_name,
                'creator_profile_pic': creator_profile.profile_picture,
                'post': post,
                'comments': comments,
            }

            return render(request, self.template_name, context=context)

        except Exception as e:
            return render(request, 'errors/error.html', {'error_message': str(e)})


def add_comment(request, post_id):
    try:
        if request.method == 'POST':
            form = CommentForm(request.POST, request.FILES)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.creator = request.user
                comment.save()
                post = get_object_or_404(Post, id=post_id)
                post.comments.add(comment)

                return redirect(f'/viewpost/{post_id}/')
        else:
            form = CommentForm()

        return render(request, 'common/add-comment.html', {'form': form, 'post_id': post_id})

    except Exception as e:
        return render(request, 'errors/error.html', {'error_message': str(e)})


class EditCommentView(LoginRequiredMixin, View):
    template_name = 'common/edit-comment.html'

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = EditCommentForm(instance=comment)

        context = {
            'form': form,
            'comment': comment,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = EditCommentForm(request.POST, request.FILES, instance=comment)


        if form.is_valid():
            form.save()
            return redirect('home page')

        context = {
            'form': form,
            'comment': comment,
        }

        return render(request, self.template_name, context=context)


class DeleteCommentView(LoginRequiredMixin, View):
    template_name = 'common/delete-comment.html'

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        context = {
            'comment': comment,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()

        return redirect('home page')

