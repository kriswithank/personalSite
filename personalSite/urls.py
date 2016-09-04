from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^finance/', include('finance.urls')),
    url(r'^notes/', include('coursenotes.urls')),
    url(r'^admin/', admin.site.urls),
]
