from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

from .models import User, SeekerProfile, OwnerProfile
from .forms import RegisterForm, LoginForm
from .utils import generate_otp, send_otp_email

# Home
def home(request):

    # properties = Property.objects.all()[:6]

    # context = {
    #     "properties":properties
    # }

    return render(request,"accounts/home.html")

# About
def about(request):

    return render(request, "accounts/about.html")

# Contact
def contact(request):

    return render(request, "accounts/contact.html")

# Register
from django.db import transaction

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic(): # Ensures both User and Profile are saved or neither
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data["password"])
                    user.save()

                    if user.role == "SEEKER":
                        otp = generate_otp()
                        SeekerProfile.objects.create(
                            user=user,
                            otp=otp,
                            otp_created_at=timezone.now()
                        )
                        send_otp_email(user, otp)
                        return redirect("verify_otp")

                    elif user.role == "OWNER":
                        OwnerProfile.objects.create(user=user)
                        messages.success(request, "Account created. Waiting for admin verification.")
                        return redirect("login")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# Verify OTP
def verify_otp(request):

    if request.method == "POST":

        email = request.POST.get("email")
        otp = request.POST.get("otp")

        try:

            user = User.objects.get(email=email)
            
            if user.role != "SEEKER":
                messages.error(request, "This account does not require OTP verification.")
                return redirect('login')

            seeker = user.seeker_profile

            if seeker.otp == otp:

                if timezone.now() - seeker.otp_created_at < timedelta(minutes=5):

                    user.is_verified = True
                    user.verification_date = timezone.now()
                    user.save()

                    messages.success(request, "Account verified successfully")

                    return redirect("login")

                else:
                    messages.error(request, "OTP expired")

            else:
                messages.error(request, "Invalid OTP")

        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "accounts/verify_otp.html")

def login_view(request):

    # If a logged-in user is not verified, force logout
    if request.user.is_authenticated and not request.user.is_verified:
        logout(request)
        messages.warning(request, "Your account is not verified.")
        return redirect("verify_otp")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:

                if not user.is_verified:

                    # Prevent login for unverified accounts
                    logout(request)

                    messages.error(
                        request,
                        "Your account is not verified. Please verify your account first."
                    )

                    return redirect("verify_otp")

                # Login only if verified
                login(request, user)

                messages.success(
                    request,
                    "Login successful."
                )

                return redirect("dashboard")

            else:

                messages.error(
                    request,
                    "Invalid username or password"
                )

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")