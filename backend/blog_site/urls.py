import os

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path(os.environ['BLOG_ADMIN_PATH'], admin.site.urls),
    path('api/accounts/', include('account.urls')),
    path('api/blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
