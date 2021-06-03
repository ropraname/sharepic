from django.forms import TextInput, ClearableFileInput
from django.forms import HiddenInput, Textarea
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
            "title": TextInput(),
            "picture": ClearableFileInput(),
            "anons": TextInput(),
            "full_text": Textarea(),
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
                'placeholder': 'Смысловая ценность'
            }),
            "rate_draw_technique": TextInput(attrs={
                'class': 'custom-range',
                'placeholder': 'Техника'
            }),
            "rate_originality": TextInput(attrs={
                'class': 'custom-range',
                'placeholder': 'Оригинальность'
            }),
            "picture_id": HiddenInput(),
        }