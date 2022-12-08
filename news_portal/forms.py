from django.forms import ModelForm
from .models import News, Evidence, Comment, ReportedNews, Ad
from django import forms


class DatePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "sub_title", "body", "image1", "image2", "image3", "source", "location", "category", "is_anonymous" ]


class EvidenceForm(ModelForm):
    class Meta:
        model = Evidence
        fields = ["image", "file1", "file2"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class ReportedNewsForm(ModelForm):
    class Meta:
        model = ReportedNews
        fields = ["description", "status"]
        
class AdRequestForm(ModelForm):
    class Meta:
        model = Ad
        fields = "__all__"
        widgets = {
            'start_date_time':forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
            'end_date_time':forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'})
        }
