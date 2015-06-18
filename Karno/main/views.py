from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.forms import YoutubeUrlForm
from main.models import YoutubeUrl


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class UserRegisteration(FormView):
    """
    Class to handle user Registeration
    Author: Moustafa
    """
    template_name = 'registration/user-registeration.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        """
        Saves user and automatically logs him/her in
        """
        form.save()
        user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
        login(self.request, user)
        messages.add_message(
                self.request, messages.INFO,
                'welcome ' + self.request.user.username + '.')
        return HttpResponseRedirect(reverse_lazy('home'))


class UserChangePassword(LoginRequiredMixin, FormView):
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


class YoutubeUrlFormView(LoginRequiredMixin, FormView):
    """
    Creates a single Youtube Url to be embeded.

    Author: Aly Yakan

    **Template:**

    :template:`main/youtubeurl_form.html`
    """
    model = YoutubeUrl
    form_class = YoutubeUrlForm
    template_name = 'main/youtubeurl_form.html'

    def form_valid(self, form):
        """
        Gets the Video ID from the Url and the current logged in user
        then saves an instance of YoutubeUrl using this information

        Author: Aly Yakan
        """
        form.save(commit=False)
        user = self.request.user
        url = form.cleaned_data['url']
        vid_id = url.split('?v=')[1]
        YoutubeUrl.objects.create(user=user, url=url, video_id=vid_id)
        return HttpResponseRedirect(reverse_lazy('youtube_video_list'))
