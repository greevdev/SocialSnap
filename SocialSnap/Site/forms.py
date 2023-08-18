from django import forms
from .models import Profile, Post, Comment


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=255, required=True)

    def save(self, commit=True):
        user = self.instance.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
