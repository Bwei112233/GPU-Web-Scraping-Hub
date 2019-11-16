
from django.urls import path, include
from scrapers import views
from scrapers.amazon_scrap.amazon_scrap.spiders.amazon_spider import call_scraper
urlpatterns = [
    path("newegg/", views.get_GPU_info_Newegg, name = "get_GPU_info_Newegg"),
    path("frys/", views.get_GPU_info_Frys, name ="get_GPU_info_Frys" ),
    path("micro/", views.get_GPU_info_MicroCenter, name = "get_GPU_info_MicroCenter"),
    path("amazon/", call_scraper, name = "call_scraper")
]
