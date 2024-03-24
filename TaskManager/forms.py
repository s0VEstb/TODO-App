from django import forms
from.models import Task, Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']