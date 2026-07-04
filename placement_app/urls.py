from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("profile/", views.profile, name="profile"),
    path("resume/", views.resume, name="resume"),
    path("analyzer/", views.analyzer, name="analyzer"),
    path("assessment/", views.assessment, name="assessment"),
    path("reports/", views.reports, name="reports"),
    path("career/", views.career, name="career"),
    path("prediction/", views.prediction, name="prediction"),
    path("interview/", views.interview, name="interview"),
    path("logout/", views.logout_view, name="logout"),
    path("api/jobs/", views.api_jobs, name="api_jobs"),
    path("jobs/", views.jobs, name="jobs"),
]