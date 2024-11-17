from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from app.forms import UserLoginForm, UserCreateForm, UserUpdateForm
from app.models import User
import os


def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            auth_login(request, user)
            return redirect("/catalog")
    else:
        form = UserCreateForm()
    return render(request, "pages/register.html", {"form": form, "title": "Daftar"})


def login(request):
    if (request.method == "POST"):
        form = UserLoginForm(request.POST)
        if (form.is_valid()):
            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                auth_login(request, user)
                return redirect("/catalog")
            else:
                messages.error(request, "Username or password is wrong")
                return redirect("/login")
    else:
        form = UserLoginForm()
    return render(request, "pages/login.html", {"title": "login", "form": form})


@login_required
def profile(request):

    if (request.method == "POST"):
        user_form = UserUpdateForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = User.objects.get(id=request.user.id)
            name = user_form.cleaned_data["name"]
            email = user_form.cleaned_data["email"]
            password = user_form.cleaned_data["password"]
            image = user_form.cleaned_data["image"]

            if name:
                user.name = name

            if email:
                user.email = email

            if password:
                user.set_password(password)

            if image:
                if user.image != 'user/profile.png':
                    fname = f'{settings.MEDIA_ROOT}/{user.image}'
                    if os.path.exists(fname):
                        os.remove(fname)
                user.image = request.FILES["image"]

            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "success update profile")
            return redirect("/profile")

    else:
        user_form = UserUpdateForm(initial={
            "email": request.user.email,
            "name": request.user.name,
            "image": request.user.image
        })

    return render(request, "pages/user_profile.html", {
        "title": "user profile",
        "user": request.user,
        "form": user_form
    })


@login_required
def logout(request):
    auth_logout(request)
    return redirect("login")
