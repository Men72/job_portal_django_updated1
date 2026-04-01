from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings

from .models import Job, Application, SavedJob
from .forms import LoginForm, JobSeekerSignupForm, EmployerSignupForm, PostJobForm, ApplicationForm


# ── Auth decorators ─────────────────────────────────────────
def employer_required(view_func):
    """Redirect non-employers (non-admin users) to home."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_employer:
            messages.error(request, 'This page is only available to employers.')
            return redirect('job_listings')
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Auth views ──────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('job_listings')

    role = request.GET.get('role', 'seeker')
    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        role = request.POST.get('role', 'seeker')
        if form.is_valid():
            user = form.get_user()

            if role == 'employer' and not user.is_employer:
                messages.error(request, 'This account is not an employer account.')
                return render(request, 'portal/login.html', {'form': form, 'role': role})
            if role == 'seeker' and user.is_employer and not user.is_admin:
                messages.error(request, 'This is an employer account. Please select Employer.')
                return render(request, 'portal/login.html', {'form': form, 'role': role})

            login(request, user)
            return redirect(request.GET.get('next', 'job_listings'))

    return render(request, 'portal/login.html', {'form': form, 'role': role})


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('job_listings')

    role = request.GET.get('role', 'seeker')
    if request.method == 'POST':
        role = request.POST.get('role', 'seeker')
        if role == 'employer':
            form = EmployerSignupForm(request.POST)
        else:
            form = JobSeekerSignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'employer':
                messages.success(request, 'Employer account created! Post your first job.')
                return redirect('post_job')
            return redirect('job_listings')
    else:
        form = EmployerSignupForm() if role == 'employer' else JobSeekerSignupForm()

    return render(request, 'portal/signup.html', {'form': form, 'role': role})


# ── Job Listings ────────────────────────────────────────────
def job_listings(request):
    jobs = Job.objects.all()
    q    = request.GET.get('q', '').strip()
    jtype = request.GET.get('type', 'all')

    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(company__icontains=q) |
            Q(location__icontains=q)
        )
    if jtype and jtype != 'all':
        jobs = jobs.filter(type=jtype)

    job_types = ['Full-time', 'Part-time', 'Contract', 'Freelance']
    return render(request, 'portal/job_listings.html', {
        'jobs': jobs,
        'q': q,
        'selected_type': jtype,
        'job_types': job_types,
    })


# ── Job Detail + Apply ──────────────────────────────────────
def job_detail(request, pk):
    job      = get_object_or_404(Job, pk=pk)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()

    app_form = ApplicationForm()
    submitted = False

    if request.method == 'POST' and 'apply' in request.POST:
        app_form = ApplicationForm(request.POST, request.FILES)
        if app_form.is_valid():
            application = app_form.save(commit=False)
            application.job = job
            if request.user.is_authenticated:
                application.applied_by = request.user
            application.save()
            submitted = True
            app_form = ApplicationForm()   # reset form

    return render(request, 'portal/job_detail.html', {
        'job': job,
        'is_saved': is_saved,
        'app_form': app_form,
        'submitted': submitted,
    })


@login_required
@require_POST
def toggle_save_job(request, pk):
    job  = get_object_or_404(Job, pk=pk)
    obj, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        obj.delete()
        saved = False
    else:
        saved = True
    return JsonResponse({'saved': saved})


# ── Post Job ────────────────────────────────────────────────
@employer_required
def post_job(request):
    form = PostJobForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)
        job.posted_by = request.user
        job.save()
        messages.success(request, 'Job posted successfully! It is now live.')
        return redirect('job_listings')

    return render(request, 'portal/post_job.html', {'form': form})


# ── Applications (admin view) ────────────────────────────────
@employer_required
def applications(request):
    # Admins see all applications; employers see only their own jobs' applications
    if request.user.is_admin:
        apps = Application.objects.select_related('job').all()
    else:
        apps = Application.objects.select_related('job').filter(job__posted_by=request.user)

    selected_status = request.GET.get('status', 'all')
    if selected_status != 'all':
        apps = apps.filter(status=selected_status)

    statuses = ['pending', 'reviewed', 'interviewed', 'accepted', 'rejected']
    return render(request, 'portal/applications.html', {
        'applications': apps,
        'statuses': statuses,
        'selected_status': selected_status,
    })


@employer_required
@require_POST
def update_application_status(request, pk):
    app = get_object_or_404(Application, pk=pk)
    status = request.POST.get('status')
    valid = [s[0] for s in Application.STATUS_CHOICES]
    if status in valid:
        app.status = status
        app.save()

        # Notify applicant when interview result is decided
        if status in ['accepted', 'rejected']:
            subject = (
                f'🎉 You passed the interview for {app.job.title}!'
                if status == 'accepted'
                else f'Application Update – {app.job.title}'
            )
            message = (
                f'Hi {app.applicant_name},\n\nCongratulations! You have been ACCEPTED for {app.job.title} at {app.job.company}.\n\nWe will contact you shortly.'
                if status == 'accepted'
                else f'Hi {app.applicant_name},\n\nThank you for interviewing for {app.job.title} at {app.job.company}. Unfortunately, you were not selected at this time.\n\nWe wish you the best.'
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [app.applicant_email], fail_silently=True)

    return redirect(f'/applications/?status={request.POST.get("current_filter", "all")}')





# ── Dashboard (user view) ────────────────────────────────────
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')

    UserModel = get_user_model()

    # Admin stats — ALL data, not just the logged-in user's
    all_jobs  = Job.objects.all()
    all_apps  = Application.objects.select_related('job', 'applied_by')
    all_users = UserModel.objects.all()

    counts = {
        'total_jobs':     all_jobs.count(),
        'total_apps':     all_apps.count(),
        'total_users':    all_users.count(),
        # Added employee/employer/admin counts
        'total_employees': all_users.filter(role='user').count(),
        'total_employers': all_users.filter(role='employer').count(),
        'total_admins':    all_users.filter(role='admin').count(),
        'pending':        all_apps.filter(status='pending').count(),
        'reviewed':       all_apps.filter(status='reviewed').count(),
        'interviewed':    all_apps.filter(status='interviewed').count(),
        'accepted':       all_apps.filter(status='accepted').count(),
        'rejected':       all_apps.filter(status='rejected').count(),
    }

    return render(request, 'portal/admin_dashboard.html', {  # ← correct template
        'recent_apps':  all_apps.order_by('-applied_date')[:5],
        'recent_jobs':  all_jobs.order_by('-posted_date')[:5],
        'recent_users': all_users.order_by('-date_joined')[:5],
        'counts':       counts,
    })


# ── Dashboard (user view) ────────────────────────────────────
@login_required
def dashboard(request):
    user  = request.user
    apps  = Application.objects.filter(applied_by=user).select_related('job')
    saved = SavedJob.objects.filter(user=user).select_related('job')[:3]

    counts = {
        'total':       apps.count(),
        'pending':     apps.filter(status='pending').count(),
        'reviewed':    apps.filter(status='reviewed').count(),
        'interviewed': apps.filter(status='interviewed').count(),
        'accepted':    apps.filter(status='accepted').count(),
        'rejected':    apps.filter(status='rejected').count(),
    }

    return render(request, 'portal/dashboard.html', {
        'recent_apps': apps[:3],
        'saved_jobs':  saved,
        'counts':      counts,
    })

# ── Edit Job ─────────────────────────────────────────────────
@employer_required
def edit_job(request, pk):
    job  = get_object_or_404(Job, pk=pk)
    form = PostJobForm(request.POST or None, instance=job)  # ✅ instance= pre-fills the form

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'"{job.title}" has been updated successfully.')
        return redirect('job_detail', pk=job.pk)

    return render(request, 'portal/edit_job.html', {
        'form': form,
        'job':  job,
    })


# ── Delete Job ────────────────────────────────────────────────
@employer_required
@require_POST
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    title = job.title
    job.delete()
    messages.success(request, f'"{title}" has been deleted.')
    return redirect('job_listings')