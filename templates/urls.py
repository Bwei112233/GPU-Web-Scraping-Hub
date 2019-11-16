from django.urls import path, include
from templates import views

urlpatterns = [
    path('', views.index, name = "index")
]
