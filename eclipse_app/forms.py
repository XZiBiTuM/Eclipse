from django import forms
from .models import *
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'profile_image']


class ArticleForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите теги через запятую'})
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'description']
        widgets = {
            'content': CKEditorWidget(),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'oninput': 'updateCharCount(this)'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        article = super().save(commit=False)

        if self.user:
            article.author = self.user

        article.save()

        tags = self.cleaned_data['tags']
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag_name in tag_list:
                tag, created = ArticleTag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)

        return article


