from django import forms
from posts.models import Post
from posts.models import Category, Tag

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'title', 'content', 'rate', 'category', 'tag']

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
    


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget = forms.TextInput(attrs={'placeholder':'Search'})
    )

    category = forms.ModelChoiceField(queryset= Category.objects.all(), 
                                      required=False, 
                                      widget = forms.Select())
    
    tegs = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), 
                                          widget=forms.CheckboxSelectMultiple
                                          )


    
    orderings = (
        ("title", "По названию"),
        ("-title", "По названию(от я до а)"),

        ("created_at", "Дата создания"),
        ("-created_at", "Дата создания(По убыванию)"),

        ("rate" , "Рейтинг"),
        ("-rate" , "Рейтинг(По убыванию)"),
    )

    ordering = forms.ChoiceField(
        choices=orderings, 
        required=False, 
        widget=forms.Select(attrs={"class": "form-control"}),
        )
    


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'content', 'rate', 'category', 'tag']
        exclude = ['created_at']