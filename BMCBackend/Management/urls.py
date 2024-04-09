from django.urls import path
import Management.views as views

urlpatterns = [
    path('summary/log/<int:year>/', views.log_data_by_year),
    path('summary/service1/<int:year>/', views.service_1_by_year),
    path('summary/service2/<int:year>/', views.service_2_by_year),
    path('summary/cpuCard/<int:year>/', views.cpu_card_by_year),
    path('summary/memCard/<int:year>/', views.memory_card_1_by_year),
    path('summary/memCard2/<int:year>/', views.memory_card_2_by_year),
]
