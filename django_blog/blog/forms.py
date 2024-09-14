from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Profile, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only include the content field for the form

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 4:
            raise forms.ValidationError("Comment is too short!")
        return content
   