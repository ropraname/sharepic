from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegistrForm, LoginForm
from django.contrib.auth import logout


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    data = {
                        'form': form,
                        'message': 'Отключенный аккаунт'
                    }
                    return render(request, 'authorization/login.html', data)
            else:
                data = {
                    'form': form,
                    'message': 'Неправильный логин или пароль'
                }
                return render(request, 'authorization/login.html', data)
    else:
        form = LoginForm()
        return render(request, 'authorization/login.html', {'form': form})


def regist(request):
    data = {}
    if request.method == 'POST':
        form = RegistrForm(request.POST)
        if form.is_valid():
            form.save()
            # Передача формы к рендару
            data = {
                'form': form,
                'message': "Всё прошло успешно"
            }
            return redirect('login')
        else:
            data = {
                'form': form,
                'message': "Неправильно заполнена форма"
            }

            return render(request, 'authorization/registr.html', data)
    else:
        form = RegistrForm()
        data['form'] = form
        return render(request, 'authorization/registr.html', data)


def user_logout(request):
    logout(request)
    return render(request, 'authorization/logged_out.html')
