from django import forms
from transliterate import slugify, translit

from .models import Cities, Announcement, TagPost

class AddPostForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=Cities.objects.all(), required=False, label="Город",  empty_label="Выберете город")
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label='Оснащение', widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'status_announcement']

