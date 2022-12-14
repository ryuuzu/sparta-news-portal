from django.forms import ModelForm
from .models import News, Evidence, Comment, ReportedNews, Ad, PortalUser
from django import forms

#date picker type
class DatePickerInput(forms.DateTimeInput):
    input_type = 'datetime'

#form for news
class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "sub_title", "body", "image1", "image2", "image3", "source", "location", "category", "is_anonymous" ]

#form for evidence
class EvidenceForm(ModelForm):
    class Meta:
        model = Evidence
        fields = ["image", "file1", "file2"]

#form for comment
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

#form for reported news
class ReportedNewsForm(ModelForm):
    class Meta:
        model = ReportedNews
        fields = ["description", "status"]
        
#form to request ad
class AdRequestForm(ModelForm):
    class Meta:
        model = Ad
        fields = "__all__"
        widgets = {
            'start_date_time':forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'}),
            'end_date_time':forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local'})
        }


class UserForm(ModelForm):
    class Meta:
        model = PortalUser
        fields = ["username", "password", "password", "email", "first_name", "middle_name", "last_name"]
