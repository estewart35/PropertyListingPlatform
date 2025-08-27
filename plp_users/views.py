from django.shortcuts import render, redirect
from .forms import ProfileForm, RegistrationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f"Welcome {first_name}! Your account was created successfully.")
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'plp_users/register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was saved successfully!")
            return redirect('profile')  # Replace with the appropriate URL name
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'plp_users/profile.html', {'form': form, 'profile': profile})
