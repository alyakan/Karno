from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls')),
    url(r'^messages/', include('postman.urls')),
    url(r'^youtube/', include('my_youtube.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
