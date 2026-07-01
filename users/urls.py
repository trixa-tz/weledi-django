from django.urls import path

from . import views

urlpatterns = [
    # HTML form pages
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # super-admin area (superusers only)
    path('super-admin/', views.super_admin, name='super_admin'),
    path('super-admin/users/<int:user_id>/toggle-auditor/', views.toggle_auditor, name='toggle_auditor'),

    # API endpoints (same style as posts api)
    path('api/auth/signup/', views.api_signup, name='api_signup'),
    path('api/auth/login/', views.api_login, name='api_login'),
]
