from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}! Login Now')
            return render(request, 'stackbase:home')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'stackusers/register.html', {'form': form})