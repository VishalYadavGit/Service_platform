from django.contrib import admin
from django.urls import path,include
from django .conf import settings
from django .conf.urls.static import static

admin.site.site_header = "PLumbtric "
admin.site.site_title = "Plumbtric Admin Portal"
admin.site.index_title = "Plumbtric"

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('', include('service_platform.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)