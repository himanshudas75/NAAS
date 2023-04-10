from django.shortcuts import redirect, render

def home(request):
    if request.user.is_authenticated:
        return redirect('users')
    return redirect('/accounts/login')