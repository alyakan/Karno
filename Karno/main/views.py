from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView, DeleteView
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
from main.models import YoutubeUrl, Comment, CommentNotification
from django.db.models.signals import post_save
from django.dispatch import receiver
from filetransfers.api import serve_file
from django.shortcuts import get_object_or_404


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


def download_handler(request, pk):
    """
    Function that handles a download request of a file
    Author: Kareem Tarek , Moustafa Mahmoud
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
        print ("Extension", extension)
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
                print "Dada Saved"

            else:
                pass
        ################
        if form.cleaned_data['group']:
            for user in self.request.POST.getlist('users'):
                GroupPermission.objects.create(
                    user=User.objects.get(id=user),
                    file_uploaded=form1)
        return super(UploadFile, self).form_valid(form)


class FileListView(ListView):

    """
    A class for listing all instances of Model:main.File
    Author: Rana El-Garem
    """
    model = File


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


class PaginateMixin(object):
    """
    A Mixin used to paginate any object_list.
    :author Nourhan Fawzy:
    :param object:
    :return:
    """

    paginate_by = 3


# login is required to add comment, however not required to display comments


class CommentListView(PaginateMixin, ListView):
    """
    A class for showing details of Model:main.Comment
    Author: Nourhan Fawzy
    """
    model = Comment

    def get_queryset(self):
        """
        Gets a queryset of comments for a certain file.
        :author Nourhan Fawzy:
        :param self:
        :return Books list for certain library:
        """
        return Comment.objects.filter(
            file_uploaded=File.objects.get(id=self.kwargs['file_id']))

    def get_context_data(self, **kwargs):
        """
        Gets details of Model:main.Comment
        :author Nourhan Fawzy:
        """

        context = super(CommentListView, self).get_context_data(**kwargs)
        context['file'] = File.objects.get(id=self.kwargs['file_id'])
        return context

    def post(self, args, **kwargs):
        """
        Adds a new comment to the database and post it
        :author Nourhan Fawzy:
        """
        file_uploaded = File.objects.get(id=self.kwargs['file_id'])
        description = self.request.POST['description']
        user = self.request.user
        comment = Comment(
            description=description, user=user,
            file_uploaded=file_uploaded)
        comment.save()
        return HttpResponseRedirect(
            reverse(
                'comment-list',
                kwargs={"file_id": file_uploaded.id}))


class NotificationListView(PaginateMixin, ListView):
    """
    Lists all notifications when a new comment is added on a file I shared.
    :author Nourhan Fawzy:
    :param PaginateMixin, ListView:
    :return:
    """

    model = CommentNotification

    def get_context_data(self, **kwargs):
        """
        Gets a list of notifications for a given user.
        :author Nourhan Fawzy:
        :param self, keyword arguments:
        :return context:
        """

        context = super(NotificationListView, self).get_context_data(**kwargs)

        unread = CommentNotification.objects.filter(
            status=0, user_notified=self.request.user.id)
        print unread
        read = CommentNotification.objects.filter(
            status=1, user_notified=self.request.user.id)

        for notification in unread:
            notification.status = 1
            notification.save()

        context['read'] = read
        context['unread'] = unread

        return context


@receiver(post_save, sender=Comment)
def create_notification(sender, **kwargs):
    """
    A function that creates a new notification once a new
    comment is added on a file I shared.
    :author Nourhan Fawzy:
    :param sender, keyword arguments:
    :return:
    """
    print kwargs
    if kwargs.get('created', False):
        comment = kwargs.get('instance')
        file_uploaded = comment.file_uploaded
        comments = Comment.objects.all().filter(file_uploaded=file_uploaded)

        # create a notification when others comment on file I commented on

        for c in comments:
            if c.user != comment.user and c.user != file_uploaded.user:
                CommentNotification.objects.create(
                    comment=comment,
                    file_shared=file_uploaded,
                    user_notified=c.user)

        CommentNotification.objects.create(
                comment=comment, file_shared=comment.file_uploaded,
                user_notified=comment.file_uploaded.user)


class CommentDelete(DeleteView):
    """
    Deletes a book model.
    :author Nourhan Fawzy:
    :param DeleteView:
    :return:
    """

    model = Comment

    def get_success_url(self):

        return reverse(
            'comment-list',
            kwargs={'file_id': self.request.user.file_uploaded.id}
                       )


class FileDetailView(DetailView):

    """
    Views a single File's detials.

    Author: Aly Yakan

    **Template:**

    :template:`main/file_detail.html`
    """
    model = File
    template_name = "main/file_detail.html"
