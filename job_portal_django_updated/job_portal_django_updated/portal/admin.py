from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Job, Application, SavedJob


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Avatar', {'fields': ('role', 'avatar')}),
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'type', 'location', 'posted_date')
    list_filter  = ('type',)
    search_fields = ('title', 'company')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'job', 'status', 'applied_date')
    list_filter  = ('status',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
