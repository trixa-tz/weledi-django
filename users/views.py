from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


# ---------------------------------------------------------------------------
# HTML form views (normal POST -> read request.POST -> create/authenticate user)
# ---------------------------------------------------------------------------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')

    if request.method == 'POST':
        # get data submitted from the form
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'That username is already taken.')
        else:
            # create a new user in the User model
            user = User.objects.create_user(
                username=username, password=password, phone=phone,
            )
            login(request, user)
            messages.success(request, f'Welcome to Weledi, {user.username}!')
            return redirect('post_list')

    return render(request, 'users/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('post_list')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('post_list')


# ---------------------------------------------------------------------------
# Super-admin area (only superusers may enter)
# ---------------------------------------------------------------------------

def _is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(_is_superuser, login_url='login')
def super_admin(request):
    users = User.objects.all().order_by('-is_superuser', '-is_auditor', 'username')
    return render(request, 'users/super_admin.html', {'users': users})


@require_POST
@user_passes_test(_is_superuser, login_url='login')
def toggle_auditor(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    target.is_auditor = not target.is_auditor
    target.save(update_fields=['is_auditor'])
    state = 'granted' if target.is_auditor else 'revoked'
    messages.success(request, f'Auditor access {state} for {target.username}.')
    return redirect('super_admin')


# ---------------------------------------------------------------------------
# API views (same @api_view style as posts) -> JSON in, JSON out
# ---------------------------------------------------------------------------

@api_view(['POST'])
def api_signup(request: Request):
    data: dict = request.data

    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone', '')

    if not username or not password:
        return Response({'detail': 'username and password are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'username already taken.'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username, password=password, phone=phone,
    )

    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def api_login(request: Request):
    data: dict = request.data

    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'detail': 'Invalid username or password.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'detail': 'Login successful.',
        'user': UserSerializer(user).data,
    })
