from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse_lazy
from main.forms import FileUploadForm
from main.models import File
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.debug import sensitive_post_parameters
from main.forms import UserForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login


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
                             "File was Uploaded successfully")
        return super(UploadFile, self).form_valid(form)


class FileListView(ListView):
    model = File


class RegisterView(FormView):

    """
    Registers a user.

    Author: Aly Yakan

    **Template:**

    :template:`main/register.html`
    """
    form_class = UserForm
    template_name = 'main/register.html'
    success_url = '/main/'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request,
                          self.template_name,
                          {'form': form,
                           'registered': registered})
        messages.error(self.request, "Invalid username or password!")
        registered = False
        return render(request, self.template_name, {'form': form,
                                                    'registered': registered})


class LoginView(FormView):

    """
    Logins a user into the system.

    Author: Aly Yakan

    **Template:**

    :template:`main/book_list.html`
    """
    form_class = AuthenticationForm
    template_name = 'main/login.html'

    def form_valid(self, form):
        # redirect_to = self.request.POST.get('next', '')
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        # if redirect_to:
        #     return HttpResponseRedirect(reverse(redirect_to))
        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        messages.error(self.request, "Wrong username or password!")
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)
