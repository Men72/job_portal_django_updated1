from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/',                  views.admin_dashboard,            name='admin_dashboard'),
    path('',                                  views.job_listings,               name='job_listings'),
    path('login/',                            views.login_view,                 name='login'),
    path('logout/',                           views.logout_view,                name='logout'),
    path('signup/',                           views.signup_view,                name='signup'),
    path('jobs/<int:pk>/',                    views.job_detail,                 name='job_detail'),
    path('jobs/<int:pk>/save/',               views.toggle_save_job,            name='toggle_save_job'),
    path('jobs/<int:pk>/edit/',               views.edit_job,                   name='edit_job'),     
    path('jobs/<int:pk>/delete/',             views.delete_job,                 name='delete_job'),   
    path('post-job/',                         views.post_job,                   name='post_job'),
    path('applications/',                     views.applications,               name='applications'),
    path('applications/<int:pk>/status/',     views.update_application_status,  name='update_application_status'),
    path('dashboard/',                        views.dashboard,                  name='dashboard'),
]
