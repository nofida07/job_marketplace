from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ----------------------------
# Job Model
# ----------------------------
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("full_time", "Full-Time"),
        ("part_time", "Part-Time"),
        ("remote", "Work From Home"),
    ]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(default="No description provided")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_type = models.CharField(max_length=20, choices=[("year", "Per Year"), ("month", "Per Month")], default="year")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full_time")
    posted_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"


# ----------------------------
# Internship Model
# ----------------------------
class Internship(models.Model):
    INTERNSHIP_TYPE_CHOICES = [
        ("onsite", "Onsite"),
        ("wfh", "Work From Home"),
    ]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    stipend = models.CharField(max_length=50, blank=True, null=True)
    internship_type = models.CharField(max_length=10, choices=INTERNSHIP_TYPE_CHOICES, default="onsite")
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"


# ----------------------------
# Unified Application Model
# ----------------------------
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications", null=True, blank=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True, related_name="applications")
    internship = models.ForeignKey('Internship', on_delete=models.CASCADE, null=True, blank=True, related_name="applications")

    # ✅ Add these back
    applicant_name = models.CharField(max_length=255, blank=True)
    applicant_email = models.EmailField(blank=True)

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.job or self.internship} ({self.status})"

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant_name', 'applicant_email', 'resume', 'cover_letter']
        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'applicant_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Write your cover letter'}),
        }

# ----------------------------
# User Profile Model
# ----------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def applications(self):
        return Application.objects.filter(user=self.user)


# ----------------------------
# Signals to auto-create Profile
# ----------------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
