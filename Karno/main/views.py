from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse_lazy
from main.forms import FileUploadForm
from main.models import File
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class UploadFile(SuccessMessageMixin, FormView):
    form_class = FileUploadForm
    success_url = reverse_lazy('file-list')
    model = File
    template_name = 'main/upload_file.html'
    sucess_message = 'File Uploaded Successfully'

    def form_valid(self, form):
        form.save(commit=True)
        messages.add_message(self.request,
                             messages.INFO,
                             "File was Uploaded successfully" )
        return super(UploadFile, self).form_valid(form)


class FileListView(ListView):
    model = File
