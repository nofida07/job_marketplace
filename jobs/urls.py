from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("create-account/", views.create_account, name="create_account"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("jobs/", views.job_list, name="job_list"),
    path("job/<int:pk>/", views.job_detail, name="job_detail"),
    path("job/<int:job_id>/apply/", views.apply_job, name="apply_job"),

    path("internships/", views.internship_list, name="internship_list"),
    path("internships/<int:pk>/", views.internship_detail, name="internship_detail"),
    path("internships/<int:pk>/apply/", views.apply_internship, name="apply_internship"),

    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    path("about/", views.about, name="about"),
    path("terms/", views.terms, name="terms"),
    path("contact/", views.contact, name="contact"),
]