from .models import Comment
from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=40)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']



class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'search'}))