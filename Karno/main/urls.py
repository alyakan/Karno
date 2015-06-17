from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from main.views import UserRegisteration, UserChangePassword
from main.views import UploadFile, FileListView


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name='main/home.html'), name='home'),
    url(r'^user/new/$', UserRegisteration.as_view(), name='user-new'),
    url(
        r'^user/logout/$', auth_views.logout,
        {'next_page': '/main/'}, name='user-logout'),
    url(r'^user/login/$', auth_views.login, name='user-login'),
    url(r'^user/manage/$', TemplateView.as_view(
        template_name='registration/manage-account.html'), name='user-manage'),
    url(r'^user/change-password/$', UserChangePassword.as_view(),
        name='user-change-password'),
    url(
        r'^user/reset/$', auth_views.password_reset,
        {'template_name': 'registration/password_reset.html'},
        name='user-reset'),
    url(
        r'^resetpassword/passwordsent/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^$', TemplateView.as_view(template_name='main/index.html'),
        name='index'),
    url(r'^upload/$', UploadFile.as_view(), name='upload'),
    url(r'^file/list$', FileListView.as_view(), name='file-list')

)
