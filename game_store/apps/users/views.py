from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from game_store.apps.users.forms import RegisterForm

def register(req):
    if req.user.is_authenticated:
        return redirect('/')

    if req.method == 'POST':
        form = RegisterForm(req.POST)

        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.user.username, password=password)

            if user is not None:
                auth_login(req, user)
                return redirect('/')
    else:
        form = RegisterForm()

    return render(req, 'register.html', {
        'form': form,
    })

def login(req):
    if req.user.is_authenticated:
        return redirect('/')

    if req.method == 'POST':
        form = AuthenticationForm(req, req.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))

            if user is not None:
                auth_login(req, user)
                return redirect('/')
    else:
        form = AuthenticationForm()

    return render(req, 'login.html', {
        'form': form,
    })

def logout(req):
    auth_logout(req)
    return redirect('/')
