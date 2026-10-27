from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import SignupForm

def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, "Account created. Welcome aboard.")
        return redirect("front")
    return render(request, "registration/signup.html", {"form": form})
