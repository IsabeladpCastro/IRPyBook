from django.urls import path 
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("", views.login, name="login"),
    path("home/", views.mainPage, name="home"),
    path("register/", views.register, name="register"),
    path("registerBook/", views.registerBook, name="registerBook"),
]