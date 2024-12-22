from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployeeSignUpForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hoş geldiniz, {username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
    else:
        form = AuthenticationForm()
    return render(request, 'employees/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yapıldı.")
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'employees/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Hesap başarıyla oluşturuldu! Hoş geldiniz, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Kayıt olurken bir hata oluştu. Lütfen bilgileri kontrol edin.")
    else:
        form = EmployeeSignUpForm()
    return render(request, 'employees/register.html', {'form': form})
