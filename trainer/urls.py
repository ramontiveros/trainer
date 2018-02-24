from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('couch/', include('couch.urls')),
    path('admin/', admin.site.urls),
]
