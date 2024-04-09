from django.urls import path, include
import Disk.views as views

urlpatterns = [
    path('analysis/<str:sn>/<str:date>/', views.disk_view),
    path('list/', views.disk_list_view)
]
