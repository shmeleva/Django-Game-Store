from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from urllib.parse import urlparse
from game_store.apps.users.forms import RegisterForm
from game_store.apps.users.models import UserProfile
from game_store.apps.users.utils import send_email, decode_base64, validate_token

def register(req):
    prev_path = urlparse(req.META.get('HTTP_REFERER')).path
    if req.session.has_key('redirect-url') and prev_path in ['/login/', '/register/']:
        next = req.session['redirect-url']
    else:
        next = req.META.get('HTTP_REFERER', '/')
        req.session['redirect-url'] = next

    if req.user.is_authenticated:
        del req.session['redirect-url']
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
        del req.session['redirect-url']
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
                del req.session['redirect-url']
                return redirect(next)
    else:
        form = AuthenticationForm()

    return render(req, 'login.html', {
        'form': form,
    })

def logout(req):
    next = req.GET.get('next', '/')
    auth_logout(req)
    return redirect(next)
