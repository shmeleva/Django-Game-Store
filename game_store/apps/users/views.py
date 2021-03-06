from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from urllib.parse import urlparse
from game_store.apps.users.forms import RegisterForm, ProfileForm, AccessTokenForm, UserTypeForm
from game_store.apps.users.models import UserProfile
from game_store.apps.users.utils import send_email, decode_base64, validate_token
from rest_framework.authtoken.models import Token


def register(req):
    prev_path = urlparse(req.META.get('HTTP_REFERER')).path
    if req.session.has_key('redirect-url') and prev_path in ['/login/', '/register/']:
        next = req.session['redirect-url']
    else:
        next = req.META.get('HTTP_REFERER', '/')
        req.session['redirect-url'] = next

    if req.user.is_authenticated:
        req.session.pop('redirect-url', None)
        return redirect(next)

    if req.method == 'POST':
        form = RegisterForm(req.POST)

        if form.is_valid():
            user = form.save()
            send_email(user)
            return render(req, 'verify_email.html', { 'new_user': True })
    else:
        form = RegisterForm()

    return render(req, 'register.html', {
        'form': form,
    })

def verify(req, encoded_uid, token):
    uid = decode_base64(encoded_uid)
    user_profile = UserProfile.objects.get(id=uid)

    if user_profile is None:
        return HttpResponse(status=404)

    if not validate_token(user_profile.user, token):
        return HttpResponse(status=400)

    user_profile.verified = True
    user_profile.save()
    return redirect('/')

def login(req):
    prev_path = urlparse(req.META.get('HTTP_REFERER')).path
    if req.session.has_key('redirect-url') and prev_path in ['/login/', '/register/']:
        next = req.session['redirect-url']
    else:
        next = req.GET.get('next', req.META.get('HTTP_REFERER', '/'))
        req.session['redirect-url'] = next

    if req.user.is_authenticated:
        req.session.pop('redirect-url', None)
        return redirect(next)

    if req.method == 'POST':
        form = AuthenticationForm(req, req.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))

            if user is not None:
                user_profile = UserProfile.get_user_profile_or_none(user)

                if user_profile is None:
                    return redirect('/login/')

                if not user_profile.verified:
                    return render(req, 'verify_email.html', { 'new_user': False })

                auth_login(req, user)
                req.session.pop('redirect-url', None)
                return redirect(next)
    else:
        form = AuthenticationForm()

    return render(req, 'login.html', {
        'form': form,
    })

@login_required(login_url='/login/')
def social_auth_redirect(req):
    next = req.session.get('redirect-url', '/')

    if req.method == 'GET':
        if req.user.userprofile.role != '':
            req.session.pop('redirect-url', None)
            return redirect(next)

        form = UserTypeForm()
        return render(req, 'social_auth_redirect.html', {
            'form': form,
        })
    
    req.user.userprofile.role = req.POST.get('role')
    req.user.userprofile.verified = True
    req.user.save()

    req.session.pop('redirect-url', None)
    return redirect(next)

def logout(req):
    next = req.GET.get('next', '/')
    auth_logout(req)
    return redirect(next)

@login_required(login_url='/login/')
def edit_profile(req):
    password_form = PasswordChangeForm(user=req.user)
    access_token_form = AccessTokenForm()

    if req.method == 'POST':
        profile_form = ProfileForm(req.POST, instance=req.user)

        if profile_form.is_valid():
            user = profile_form.save()
            profile_form = ProfileForm(instance=user)
    else:
        profile_form = ProfileForm(instance=req.user)

    return render(req, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'access_token_form': access_token_form,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
    })

@login_required(login_url='/login/')
def change_password(req):
    if req.method != 'POST':
        return HttpResponse(status=404)

    form = PasswordChangeForm(req.user, req.POST)
    access_token_form = AccessTokenForm()

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(req, user)
        return redirect('/profile/edit/')

    return render(req, 'profile.html', {
        'profile_form': ProfileForm(instance=req.user),
        'password_form': form,
        'access_token_form': access_token_form,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
    })

@login_required(login_url='/login/')
def generate_access_token(req):
    if req.method != 'POST':
        return HttpResponse(status=404)

    profile_form = ProfileForm(instance=req.user)
    password_form = PasswordChangeForm(user=req.user)

    user = UserProfile.get_user_profile_or_none(req.user)
    if user and user.is_developer:
        token, _ = Token.objects.get_or_create(user=req.user)
        access_token_form = AccessTokenForm(initial={'access_token': token.key})
    else:
        return HttpResponse(status=403)

    return render(req, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'access_token_form': access_token_form,
        'user_profile': UserProfile.get_user_profile_or_none(req.user),
    })
