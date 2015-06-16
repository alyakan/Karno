from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from main.views import UploadFile, FileListView

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='main/index.html'),
        name='index'),
    url(r'^upload/$', UploadFile.as_view(), name='upload'),
    url(r'^file/list$', FileListView.as_view(), name='file-list')

    )
