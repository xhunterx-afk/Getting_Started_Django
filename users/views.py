from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Register a user


def register(request):

    # Checking a method

    if request.method != 'POST':
        form = UserCreationForm()

    else:
        # temp saving data
        form = UserCreationForm(data=request.POST)

        # saving the valid data
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            # redirect the user to the main page with the data
            return redirect('learning_logs:index')
    # Displaying the function
    context = {'form': form}
    return render(request, 'registration/register.html', context)
