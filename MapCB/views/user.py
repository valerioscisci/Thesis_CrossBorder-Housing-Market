from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect

from MapCB.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            group = form.cleaned_data['groups']
            g = Group.objects.get(name = group)
            new_user.groups.add(g)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def AreaPersonaleView(request):
    if request.method == 'POST':
        print("POST")
    else:
        print("GET")
    user = User.objects.get(username=request.user)
    return render(request, 'area_personale.html', {'user': user})
