from .forms import ProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Job, Application, Internship, Profile
from .forms import ApplicationForm, JobForm, CreateAccountForm
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import ProfileForm


class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get("username").lower()
        password = form.cleaned_data.get("password")

        user = authenticate(
            self.request,
            username=username,
            password=password
        )

        if user is not None:
            login(self.request, user)
            return redirect("home")
        else:
            return self.form_invalid(form)

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
            user = form.save(commit=False)
            user.username = form.cleaned_data["username"].lower()
            user.set_password(form.cleaned_data["password1"])  # ✅ hash password
            user.save()

            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "mobile": form.cleaned_data["mobile"],
                    "dob": form.cleaned_data["dob"],
                    "profile_picture": form.cleaned_data.get("profile_picture"),
                }
            )

            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")  # ✅ go to login page
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
            messages.success(request, f"Welcome, {request.user.first_name}!")
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
            messages.success(request, f"Welcome, {request.user.first_name}!")
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
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            return redirect("profile")
    else:
        form = ApplicationForm()
    return render(request, "apply_job.html", {"form": form, "job": job})

@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.internship = internship
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("profile")
    else:
        form = ApplicationForm()
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
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("home")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    job_applications = Application.objects.filter(user=request.user, job__isnull=False)
    internship_applications = Application.objects.filter(user=request.user, internship__isnull=False)

    return render(request, "profile.html", {
        "profile": profile,
        "job_applications": job_applications,
        "internship_applications": internship_applications,
    })