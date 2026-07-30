from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

def debug_view(request):
    return HttpResponse("OK")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('debug/', debug_view),
    path('api/', include('courses.urls')),
    path('api/users/', include('users.urls')),
]