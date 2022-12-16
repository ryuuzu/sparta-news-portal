from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from slugify import slugify
from .models import News, Evidence, Comment, PortalUser, ReportedNews, Ad, Reporter
from django import forms

# date picker type
class DatePickerInput(forms.DateTimeInput):
    input_type = "datetime"


# form for news
class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = [
            "title",
            "sub_title",
            "body",
            "image1",
            "image2",
            "image3",
            "source",
            "location",
            "category",
            "is_anonymous",
        ]
    
    def save(self,author: Reporter, commit: bool = ...):
        self.instance.slug = slugify(self.instance.title)
        self.instance.created_by = author
        return super().save(commit)


# form for evidence
class EvidenceForm(ModelForm):
    class Meta:
        model = Evidence
        fields = ["image", "file1", "file2"]


# form for comment
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


# form for reported news
class ReportedNewsForm(ModelForm):
    class Meta:
        model = ReportedNews
        fields = ["description", "status"]


# form to request ad
class AdRequestForm(ModelForm):
    class Meta:
        model = Ad
        fields = "__all__"
        widgets = {
            "start_date_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M:%S", attrs={"type": "datetime-local"}
            ),
            "end_date_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M:%S", attrs={"type": "datetime-local"}
            ),
        }


# user registration form
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField()
    last_name = forms.CharField(required=True)

    class Meta:
        model = PortalUser
        fields = (
            "username",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.middle_name = self.cleaned_data["middle_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
