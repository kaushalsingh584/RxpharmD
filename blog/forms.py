from django import forms
from django.forms import widgets
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = {'author','title','text','snippet'}


        # to change styling of a particular section eg : button color
        widgets = {
            # 'title' : forms.TextInput(attrs = {'class':'textInputClass'}),
            # 'text'  : forms.Textarea(attrs = {'class' :'editable medium-editor-textarea postcontent'})
        # there are 3 classes total in text
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = {'author','text'}

        widgets = {
            'author' : forms.TextInput(attrs = { 'class' : 'textInputClass'}),
            'text' : forms.Textarea(attrs = {'class' : 'editable medium-editor-Textarea '})
        }
