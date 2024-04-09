from django.urls import path
import Log.views as views

urlpatterns = [
    path('response_test/', views.response_test),

    path('server_status_update/', views.server_status_update),

    path('server_log_data_receiver/', views.server_log_data_receiver),
    path('memory_log_data_receiver/', views.memory_log_data_receiver),
    path('pcie_log_data_receiver/', views.pcie_log_data_receiver),
    path('disk_log_data_receiver/', views.disk_log_data_receiver),

    path('server_index/<int:year>/<int:month>/', views.server_index),
    path('memory_index/<int:year>/<int:month>/', views.memory_index),
    path('pcie_index/<int:year>/<int:month>/', views.pcie_index),

    path('log_detail/<int:id>/', views.log_detail),
]
