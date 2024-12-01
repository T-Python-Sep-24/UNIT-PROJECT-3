from django import forms
from .models import Blog,Comment
from django.contrib.auth.models import User
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'content', 'url_video', 'language']

    # optional field for selecting the writer
    written_by = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"