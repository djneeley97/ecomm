from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views import View
from django.contrib.auth import logout

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form":form})

class Login(LoginView):
    template_name =  'register/login.html'

    def get_success_url(self):
        return reverse('store')
    

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')