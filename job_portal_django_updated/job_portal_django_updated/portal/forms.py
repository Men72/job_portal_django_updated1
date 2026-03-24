from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Job, Application


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'autofocus': True})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )


class JobSeekerSignupForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Doe'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        if p1 and len(p1) < 6:
            self.add_error('password', 'Password must be at least 6 characters.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.role = 'user'
        user.set_password(self.cleaned_data['password'])
        user.avatar = 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop'
        if commit:
            user.save()
        return user


class EmployerSignupForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Company Contact Name'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'name@company.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        if p1 and len(p1) < 6:
            self.add_error('password', 'Password must be at least 6 characters.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.role = 'employer'
        user.set_password(self.cleaned_data['password'])
        user.avatar = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop'
        if commit:
            user.save()
        return user


class PostJobForm(forms.ModelForm):
    class Meta:
        model  = Job
        fields = ['title', 'company', 'location', 'type', 'salary', 'description', 'requirements']
        widgets = {
            'title':        forms.TextInput(attrs={'placeholder': 'e.g. Senior Frontend Developer'}),
            'company':      forms.TextInput(attrs={'placeholder': 'e.g. Acme Corporation'}),
            'location':     forms.TextInput(attrs={'placeholder': 'e.g. San Francisco, CA or Remote'}),
            'salary':       forms.TextInput(attrs={'placeholder': 'e.g. $100,000 – $140,000'}),
            'description':  forms.Textarea(attrs={'rows': 6, 'placeholder': 'Describe the role and responsibilities…'}),
            'requirements': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Enter each requirement on a new line'}),
        }
        labels = {
            'requirements': 'Requirements (one per line)',
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['applicant_name', 'applicant_email', 'applicant_phone', 'resume', 'cover_letter']
        widgets = {
            'applicant_name':  forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'applicant_email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'applicant_phone': forms.TextInput(attrs={'placeholder': '555-0123'}),
            'resume':          forms.FileInput(),
            'cover_letter':    forms.Textarea(attrs={'rows': 6, 'placeholder': "Tell us why you're a great fit…"}),
        }
        labels = {
            'applicant_name':  'Full Name',
            'applicant_email': 'Email Address',
            'applicant_phone': 'Phone Number',
            'resume':          'Resume / CV filename',
            'cover_letter':    'Cover Letter',
        }
