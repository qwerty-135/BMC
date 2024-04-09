from django.urls import include, path

urlpatterns = [
    path('logquery/', include("Log.urls"), name='log'),
    path('management/', include("Management.urls"), name='management'),
    path('disk/', include("Disk.urls"), name='disk'),
]
