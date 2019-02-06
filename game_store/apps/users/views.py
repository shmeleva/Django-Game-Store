from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from urllib.parse import urlparse
from game_store.apps.users.forms import RegisterForm

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
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.user.username, password=password)

            if user is not None:
                auth_login(req, user)
                del req.session['redirect-url']
                return redirect(next)
    else:
        form = RegisterForm()

    return render(req, 'register.html', {
        'form': form,
    })

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
