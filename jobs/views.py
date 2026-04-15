from .forms import ProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Job, Application, Internship, InternshipApplication, Profile
from .forms import ApplicationForm, JobForm, CreateAccountForm
from .forms import InternshipApplicationForm
from .models import Profile
from .forms import CreateAccountForm


# Home
def home(request):
    featured_jobs = Job.objects.filter(featured=True).order_by('-posted_at')[:3]
    featured_internships = Internship.objects.filter(featured=True).order_by('-posted_at')[:3]
    return render(request, "home.html", {
        "jobs": featured_jobs,
        "internships": featured_internships,
    })


# Create Account (custom form)
def create_account(request):
    if request.method == "POST":
        form = CreateAccountForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Save extra fields into Profile
            user.profile.mobile = form.cleaned_data.get("mobile")
            user.profile.dob = form.cleaned_data.get("dob")
            user.profile.profile_picture = form.cleaned_data.get("profile_picture")
            user.profile.save()

            login(request, user)
            messages.success(request, "Registered successfully!")
            return redirect("home")
    else:
        form = CreateAccountForm()
    return render(request, "create_account.html", {"form": form})

# Register (basic Django form)

def register(request):
    if request.method == "POST":
        form = CreateAccountForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]

            # ✅ Hash the password before saving
            user.set_password(form.cleaned_data["password1"])
            user.save()

            # Save Profile fields
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "mobile": form.cleaned_data["mobile"],
                    "dob": form.cleaned_data["dob"],
                    "profile_picture": form.cleaned_data.get("profile_picture"),
                }
            )

            # Log the user in immediately after registration
            login(request, user)
            return redirect("home")
    else:
        form = CreateAccountForm()
    return render(request, "create_account.html", {"form": form})
    
# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("home")

# Jobs
def job_list(request):
    query = request.GET.get("q")
    jobs = Job.objects.all().order_by("-posted_at")
    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(company__icontains=query) | jobs.filter(location__icontains=query)
    return render(request, "job_list.html", {"jobs": jobs})

def job_detail(request, pk):
    job = Job.objects.get(pk=pk)
    return render(request, "job_detail.html", {"job": job})



# jobs/views.py

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user   # ✅ attach logged-in user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("profile")
    else:
        form = ApplicationForm()
    return render(request, "apply_job.html", {"form": form, "job": job})


def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == "POST":
        form = InternshipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.internship = internship
            application.user = request.user   # ✅ attach logged-in user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("profile")
    else:
        form = InternshipApplicationForm()
    return render(request, "apply_internship.html", {"form": form, "internship": internship})


# Internships
def internship_list(request):
    internships = Internship.objects.all()
    return render(request, "internship_list.html", {"internships": internships})


def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, "internship_detail.html", {"internship": internship})

# Static pages
def about(request):
    return render(request, "about.html")

def terms(request):
    return render(request, "terms.html")

def contact(request):
    return render(request, "contact.html")



@login_required
def edit_profile(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})


@login_required
def profile_view(request):
    job_applications = Application.objects.filter(user=request.user, job__isnull=False)
    internship_applications = Application.objects.filter(user=request.user, internship__isnull=False)
    return render(request, "profile.html", {
        "job_applications": job_applications,
        "internship_applications": internship_applications,
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']  # user enters the password they set
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')