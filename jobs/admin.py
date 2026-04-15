from django.contrib import admin
from .models import Job, Application
from .models import Internship

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "posted_at")
    search_fields = ("title", "company", "location")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant_name", "job", "applied_at")
    search_fields = ("applicant_name", "applicant_email")


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "duration", "stipend", "internship_type", "posted_at")
    list_filter = ("company", "location", "internship_type")
    search_fields = ("title", "company", "location")