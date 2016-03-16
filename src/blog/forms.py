from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(
    	widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=255
    )
    content = forms.CharField(
    	widget=forms.Textarea(attrs={'class':'form-control'}), 
        max_length=4000
    )
    tags = forms.CharField(
    	widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255,
        required=False,
    )

    class Meta:
        model = Blog
        fields = [
        	'title', 
        	'content', 
        	'tags',
            'status',
        ]