from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from game_store.apps.users.forms import RegisterForm

def register(req):
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
    return render(req, 'login.html')
