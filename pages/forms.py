# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from pages.models import Article, Figure, Attachment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'style':"width:70%"})
        }
        
class FigureForm(forms.ModelForm):
    class Meta:
        model = Figure
        fields = ['primary', 'image', 'article', 'uploaded_by']
        
class AttachmentForm(forms.ModelForm):
    uploaded_by = forms.ModelChoiceField(label=u'上传者', queryset=User.objects.all(), empty_label=None)
 
    class Meta:
        model = Attachment
        fields = ['desc', 'file', 'uploaded_by']
        
