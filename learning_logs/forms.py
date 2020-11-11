from django import forms

from .models import Topic, Entry

# Adding a new topic


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['text', 'image']
        labels = {'text': ''}

# Adding new entry/info


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 100})}
