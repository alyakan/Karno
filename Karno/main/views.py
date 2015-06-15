from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages


# Create your views here.
class UserRegisteration(CreateView):
    """
    Class to handle user Registeration
    Author: Moustafa
    """
    def get(self, request, *args, **kwargs):
        """
        Initializes form for user registeration
        Author: Moustafa
        """
        form = UserCreationForm()
        return render(
            request, 'registration/user-registeration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Validated Registeration form and auto-login the new user.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password1'])
            login(request, user)
            messages.add_message(
                self.request, messages.INFO,
                'welcome ' + request.user.username + '.')
            return HttpResponseRedirect(reverse('home'))
        return render(
            request, 'registration/user-registeration.html', {'form': form})


class UserChangePassword(FormView):
    """
    Class to allow user to change his/her password.
    Author: Moustafa
    """
    def get(self, request, *args, **kwargs):
        """
        Initializes form for user registeration
        Author: Moustafa
        """
        form = PasswordChangeForm(user=request.user)
        return render(
            request, 'registration/user-change-password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Validated Registeration form and auto-login the new user.
        Author: Moustafa
        """
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.add_message(
                self.request, messages.INFO,
                'Your Password Has Been Changed Succesfuly.')
            return HttpResponseRedirect(reverse('home'))
        return render(
            request, 'registration/user-change-password.html', {'form': form})
