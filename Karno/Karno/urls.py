from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls')),
<<<<<<< HEAD

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
    url(r'^select2/', include('django_select2.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 759beab7abf96979692f7974e0dab62cb6f3fb79
