from django import forms
from .models import Complaint, Remark


class ComplaintForm(forms.ModelForm):
    class Meta:
        model  = Complaint
        fields = ['student_name', 'room_number', 'category', 'priority', 'description']
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. A-204',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe your complaint in detail...',
                'rows': 4,
            }),
        }


class RemarkForm(forms.ModelForm):
    class Meta:
        model  = Remark
        fields = ['student_name', 'content']
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Add your remark or experience...',
                'rows': 3,
            }),
        }


class SatisfactionForm(forms.Form):
    satisfaction = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput(attrs={'id': 'satisfaction-input'}),
    )