from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse_lazy
from main.forms import FileUploadForm
from main.models import File, GroupPermission
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin


class UploadFile(SuccessMessageMixin, FormView):
    """
    A class responsible for uploading a file
    and creating an instance of Model:main.File
    Author: Rana El-Garem
    """
    form_class = FileUploadForm
    success_url = reverse_lazy('file-list')
    model = File
    template_name = 'main/upload_file.html'
    success_message = 'File was Uploaded Successfully'

    def get_context_data(self, **kwargs):
        context = super(UploadFile, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

    def form_valid(self, form, **kwargs):
        """
        Saves the form,
        Creates a GroupPermission instance for each user in 'users' list
        when File.group is set to True
        Author: Rana El-Garem
        """
        form1 = form.save(commit=True)
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
