from django import forms
from .models import Application, Job, Internship, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InternshipApplication


class CreateAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username",  "first_name", "last_name", "email", "password1", "password2", "mobile", "dob", "profile_picture"]

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ["title", "company", "location", "duration", "stipend", "internship_type", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "duration": forms.TextInput(attrs={"class": "form-control"}),
            "stipend": forms.TextInput(attrs={"class": "form-control"}),
            "internship_type": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company", "location", "description", "salary", "salary_type", "job_type"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "salary": forms.NumberInput(attrs={"class": "form-control"}),
            "salary_type": forms.Select(attrs={"class": "form-select"}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
        }

# Application form
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant_name', 'applicant_email','resume']
        widgets = {
            "applicant_name": forms.TextInput(attrs={"class": "form-control"}),
            "applicant_email": forms.EmailInput(attrs={"class": "form-control"}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ["full_name", "email", "mobile", "resume", "cover_letter"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "cover_letter": forms.Textarea(attrs={"class": "form-control"}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["mobile", "dob", "profile_picture"]
        widgets = {
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "dob": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


