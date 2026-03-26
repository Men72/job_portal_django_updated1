from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    objects = UserManager()
    ROLE_CHOICES = [
        ('user', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    avatar = models.URLField(
        blank=True,
        default='https://cdn-icons-png.flaticon.com/512/3789/3789820.png'
    )

    @property
    def is_employer(self):
        return self.role in ('employer', 'admin')

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username


class Job(models.Model):
    TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
    ]
    title       = models.CharField(max_length=200)
    company     = models.CharField(max_length=200)
    location    = models.CharField(max_length=200)
    type        = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Full-time')
    salary      = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(help_text='One requirement per line')
    logo        = models.URLField(
        blank=True,
        default='https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=100&h=100&fit=crop'
    )
    posted_date = models.DateField(auto_now_add=True)
    posted_by   = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='posted_jobs'
    )

    class Meta:
        ordering = ['-posted_date']

    def get_requirements_list(self):
        return [r.strip() for r in self.requirements.splitlines() if r.strip()]

    def days_ago(self):
        from django.utils import timezone
        delta = timezone.now().date() - self.posted_date
        return delta.days

    def __str__(self):
        return f'{self.title} @ {self.company}'


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('reviewed',    'Reviewed'),
        ('interviewed', 'Interviewed'),
        ('accepted',    'Accepted'),
        ('rejected',    'Rejected'),
    ]
    job             = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant_name  = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    applicant_phone = models.CharField(max_length=50)
    resume          = models.FileField(upload_to='resumes/', help_text='Upload your resume/CV')
    cover_letter    = models.TextField()
    applied_date    = models.DateField(auto_now_add=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_by      = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='applications'
    )

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f'{self.applicant_name} → {self.job.title}'


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job  = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f'{self.user} saved {self.job}'
