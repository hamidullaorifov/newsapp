from django import forms
from blog.models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control',}),
            'password1':forms.PasswordInput(attrs={'class':'form-control',}),
            'password2':forms.PasswordInput(attrs={'class':'form-control',})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['publish','slug','author','created','updated']
        widgets = {
            'picture':forms.URLInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control',}),
            'body':forms.Textarea(attrs={'class':'form-control',}),
            'category':forms.Select(attrs={'class':'form-control',}),
            'status':forms.Select(attrs={'class':'form-control',}),
            'tags':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter comma separated lis of tags'})}
    # tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter comma separated lis of tags'}),validators=[tags_validator])


