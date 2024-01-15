from django.urls import path 
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("home/", views.mainPage, name="home"),
    path("register/", views.register, name="register"),
    path("registerBook/", views.registerBook, name="registerBook"),
    path("book_search/", views.book_search, name="book_search"),
    path("delete_book/<int:livro_id>", views.delete_book, name="delete_book"),
    path("meusLivros/", views.meusLivros, name="meusLivros"),
    path("meuPerfil/", views.meuPerfil, name="meuPerfil"),
    path('logout/', views.fazerLogout, name="logout"),
]