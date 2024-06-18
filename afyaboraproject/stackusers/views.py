from django.shortcuts import render
from django.contrib.auth.forms import   UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}! Login Now')
            return render(request, 'home.html')
    else:
        form = UserCreationForm()
        
    return render(request, 'stackusers/register.html', {'form': form})