from django.forms import TextInput, ClearableFileInput
from django.forms import HiddenInput
from django.forms import ModelForm
from .models import Grading
from .models import Picture


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['current_user', 'title', 'anons',
                  'picture', 'full_text', 'date']

        widgets = {
            "current_user": HiddenInput(),
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название рисунка'
            }),
            "picture": ClearableFileInput(attrs={
                'class': 'form-control-file',
                'placeholder': 'Загрузка рисунка'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание рисунка'
            }),
            "full_text": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Полное описание рисунка'
            }),
            "date": HiddenInput(),
        }


class GradingForm(ModelForm):
    class Meta:
        model = Grading
        fields = ['evaluating_user', 'rate_content_meaning',
                  'rate_draw_technique', 'rate_originality', 'picture_id']

        widgets = {
            "evaluating_user": HiddenInput(),
            "rate_content_meaning": TextInput(attrs={
                'class': 'custom-range',
                'placeholder': 'Название рисунка'
            }),
            "rate_draw_technique": TextInput(attrs={
                'class': 'custom-range',
                'placeholder': 'Загрузка рисунка'
            }),
            "rate_originality": TextInput(attrs={
                'class': 'custom-range',
                'placeholder': 'Краткое описание рисунка'
            }),
            "picture_id": HiddenInput(),
        }
