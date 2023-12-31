from django.urls import path 
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("home/", views.mainPage, name="home"),
    path("register/", views.register, name="register"),
    path("registerBook/", views.registerBook, name="registerBook"),
    path("book_search/", views.book_search, name="book_search"),
]