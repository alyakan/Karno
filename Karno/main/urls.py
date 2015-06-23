from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from main.views import UserRegisteration, UserChangePassword
from main.views import (
    CommentListView, NotificationListView, CommentDelete,
    FileDelete, UploadFile, FileListView, AudioUpdate,
    FileDetailView, preview_image, YoutubeUrlFormView,
    download_handler, LikeFile, UnlikeFile, LikesListView,
    ProfileView, UploadProfileImage, ProfileImageDelete,
    TagListView, TagDetailView)


urlpatterns = patterns(
    '',
    url(r'^$', FileListView.as_view(),
        name='index'),
    url(r'^upload/$', UploadFile.as_view(), name='upload'),
    url(r'^file/list$', FileListView.as_view(), name='file-list'),
    url(r'^$', TemplateView.as_view(
        template_name='main/home.html'), name='home'),
    url(r'^user/new/$', UserRegisteration.as_view(), name='user-new'),
    url(
        r'^user/logout/$', auth_views.logout,
        {'next_page': '/main/file/list'}, name='user-logout'),
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
        {'template_name': 'registration/reset_done.html'},
        name='password_reset_done'),
    url(
        r'^add/youtubeurl/$',
        YoutubeUrlFormView.as_view(),
        name='youtubeurl-add'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/confirm_reset.html'},
        name='password_reset_confirm'),

    url(r'^$', TemplateView.as_view(template_name='main/index.html'),
        name='index'),

    url(r'^upload/$', UploadFile.as_view(), name='upload'),
    url(r'^file/list$', FileListView.as_view(), name='file-list'),

    url(
        r'^reset/done/$', auth_views.login,
        name='password_reset_complete'),
    url(r'^file/comment-list/(?P<file_id>\d+)$',
        CommentListView.as_view(), name='comment-list'),

    url(r'^file/comment/delete/(?P<pk>[-\w]+)$',
        CommentDelete.as_view(), name='delete-comment'),

    url(
        r'^notification/list/(?P<user_id>\d+)/$',
        NotificationListView.as_view(), name='notification-list'),
    url(
        r'audio/(?P<pk>[0-9]+)/update/$',
        AudioUpdate.as_view(), name='audio-update'),
    url(r'^file_download/(?P<pk>\d+)/$',
        download_handler, name='download-file'),
    url(
        r'^file/detail/(?P<pk>[0-9]+)/$',
        FileDetailView.as_view(), name="file-detail"),

    url(r'^file/delete/(?P<pk>[-\w]+)$',
        FileDelete.as_view(), name='delete-file'),

    url(
        r'^like/file/$',
        LikeFile.as_view(), name="like-file"),
    url(
        r'^unlike/file/$',
        UnlikeFile.as_view(), name="unlike-file"),
    url(
        r'^likes/list/(?P<pk>[0-9]+)$',
        LikesListView.as_view(), name="likes-list"),
    url(
        r'^preview/$', preview_image, name="preview"),
    url(r'^profile/(?P<pk>[0-9]+)/$', ProfileView.as_view(), name="profile"),

    url(r'^profile/upload/$', UploadProfileImage.as_view(),
        name="profile-upload"),

    url(r'^profile/image/delete/(?P<pk>[-\w]+)/$',
        ProfileImageDelete.as_view(), name='image-delete'),
    url(r'^tag/list$', TagListView.as_view(), name='tag-list'),
    url(r'^tag/(?P<pk>[0-9]+)/$', TagDetailView.as_view(), name='tag-detail'),



)
