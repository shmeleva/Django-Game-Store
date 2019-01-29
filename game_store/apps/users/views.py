from django.shortcuts import render
from game_store.apps.users.forms import RegisterForm

def register(req):
    form = RegisterForm()
    return render(req, 'register.html', {
        'form': form,
    })
    # if req.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # else:
    #     # TODO: Show registration form
    #     return

def login(req):
    return render(req, 'login.html')
