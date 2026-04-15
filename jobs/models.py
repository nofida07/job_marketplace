from django.db import models
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
    salary_type = models.CharField(
        max_length=10,
        choices=[("year", "Per Year"), ("month", "Per Month")],
        default="year"
    )
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full_time")
    posted_at = models.DateTimeField(auto_now_add=True)

    # ✅ New field
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"


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

    # ✅ New field
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"



# ----------------------------
# Internship Application Model
# ----------------------------
class InternshipApplication(models.Model):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, blank=True, null=True)
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"





# ----------------------------
# Job Application Model
# ----------------------------
# jobs/models.py
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True)
    internship = models.ForeignKey('Internship', on_delete=models.CASCADE, null=True, blank=True)
    applicant_name = models.CharField(max_length=255, blank=True)   # ✅ new field
    applicant_email = models.EmailField(blank=True)                 # ✅ new field
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.job or self.internship} ({self.status})"
 


# ----------------------------
# User Profile Model
# ----------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


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
