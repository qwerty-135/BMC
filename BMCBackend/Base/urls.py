from django.urls import path, include
import Base.views as views

urlpatterns = [
    path('', views.index),
]
