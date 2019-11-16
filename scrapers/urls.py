
from django.urls import path, include
from scrapers import views

urlpatterns = [
    path("newegg/", views.get_GPU_info_Newegg, name = "get_GPU_info_Newegg"),
    path("frys/", views.get_GPU_info_Frys, name ="get_GPU_info_Frys" ),
    path("micro/", views.get_GPU_info_MicroCenter, name = "get_GPU_info_MicroCenter")
]
