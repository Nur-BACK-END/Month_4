from django import forms
from posts.models import Post
from posts.models import Category



class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image','title', 'content']

    def clean(self): 
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if (title and content) and title.lower() == content.lower():
            raise forms.ValidationError('Название или описание должны быть разными')
        return cleaned_data
    

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and title.lower() =='python':
            raise forms.ValidationError('Название или описание должны быть разными')
        return title