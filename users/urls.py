from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # HTML form pages
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # super-admin area (superusers only)
    path('super-admin/', views.super_admin, name='super_admin'),
    path('super-admin/users/<uuid:user_id>/toggle-editor/', views.toggle_editor, name='toggle_editor'),

    # API endpoints (same style as posts api)
    path('api/auth/signup/', views.api_signup, name='api_signup'),
    path('api/auth/login/', views.api_login, name='api_login'),
    
    # DRF's built-in: POST {username, password} -> {token}
    path('api/auth/token/', obtain_auth_token, name='api_token'),
]
