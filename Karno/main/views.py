from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from main.forms import FileUploadForm, AudioFileUploadForm
from main.models import File, GroupPermission, AudioFile
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from main.forms import YoutubeUrlForm
from main.models import YoutubeUrl
from filetransfers.api import serve_file
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View
import json
from django.http import HttpResponse


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


def download_handler(request, pk):
    """
    Function that handles a download request of a file
    Author: Kareem Tarek , Moustafa Mahmoud`
    """
    upload = get_object_or_404(File, pk=pk)
    return serve_file(request, upload.file_uploaded, save_as=True)


class UploadFile(LoginRequiredMixin, SuccessMessageMixin, FormView):

    """
    A class responsible for uploading a file
    and creating an instance of Model:main.File
    Author: Rana El-Garem
    """
    form_class = FileUploadForm
    audio_form = AudioFileUploadForm(prefix="audioform")
    success_url = reverse_lazy('file-list')
    model = File
    template_name = 'main/upload_file.html'
    success_message = 'File was Uploaded Successfully'

    def get_context_data(self, **kwargs):
        context = super(UploadFile, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['audioform'] = self.audio_form
        return context

    def form_valid(self, form, **kwargs):
        """
        Saves the form,
        Creates a GroupPermission instance for each user in 'users' list
        when File.group is set to True
        Author: Rana El-Garem

        Creates an AudioFile instance if extension returned in
        file_uploaded.url is supported.
        Author: Kareem Tarek
        """
        form1 = form.save(commit=True)
        #  Handling Extensions #
        extension = form1.file_uploaded.url.split(".")[-1]
        if (extension == "mp3"
                or extension == "mp4"
                or extension == "ogg"
                or extension == "wav"):
            audio_form = AudioFileUploadForm(
                self.request.POST, prefix='audioform')
            if audio_form.is_valid():
                aud = audio_form.save(commit=False)
                aud.source_file = form1
                audio_form.save()
            else:
                pass
        ################
        if form.cleaned_data['group']:
            for user in self.request.POST.getlist('users'):
                GroupPermission.objects.create(
                    user=User.objects.get(id=user),
                    file_uploaded=form1)
        return super(UploadFile, self).form_valid(form)


class FileListView(View):

    """
    A class responsible for listing files with respect to their category
    Author: Kareem Tarek .

    """

    def get(self, request):
        if request.is_ajax():
            context = {}
            object_list = []
            category = request.GET['category']
            files = File.objects.all()
            for file in files:
                extension = file.file_uploaded.url.split(".")[-1]
                if ((extension == "mp3"
                     or extension == "ogg"
                     or extension == "wav")
                        and category == "audio"):
                    object_list.append(file)
                elif ((extension == "jpeg"
                       or extension == "jpg"
                       or extension == "png")
                        and category == "images"):
                    object_list.append(file)
                elif ((extension == "mov"
                        and category == "videos")):
                    object_list.append(file)
                elif ((extension == "pdf"
                        and category == "documents")):
                    object_list.append(file)
            context['object_list'] = object_list

            return HttpResponse(render_to_response('main/file_list.html',
                                                   context,
                                                   context_instance=RequestContext(request)))
        else:
            context = {}
            context['object_list'] = File.objects.all()
            return render_to_response('main/file_list.html',
                                      context,
                                      context_instance=RequestContext(request))


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


class AudioUpdate(LoginRequiredMixin, UpdateView):

    """
    Display a update form for :model:`main.AudioFile`.

    **Context**

    ``form``
         form for :model:`main.AudioFile`.

    **Template:**

    :template:`main/audio_update_form.html`

    """
    model = AudioFile
    form_class = AudioFileUploadForm
    template_name = 'main/audio_update_form.html'

    # TODO: possibly just use success_url?
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('index'))


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


class FileDetailView(DetailView):

    """
    Views a single File's detials.

    Author: Aly Yakan

    **Template:**

    :template:`main/file_detail.html`
    """
    model = File
    template_name = "main/file_detail.html"
