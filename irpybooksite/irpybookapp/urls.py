from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("home/", views.mainPage, name="home"),
    path("register/", views.register, name="register"),
    path("registerBook/", views.registerBook, name="registerBook"),
    path("book_search/", views.book_search, name="book_search"),
    path("delete_book/<int:livro_id>", views.delete_book, name="delete_book"),
    path('adicionar-livro/', views.adicionar_livro, name='adicionar_livro'),
    path("meusLivros/", views.meusLivros, name="meus_livros"),
    path("meuPerfil/", views.meuPerfil, name="meuPerfil"),
    path('logout/', views.fazerLogout, name="logout"),
    path('social/', include('social_django.urls', namespace='social')),
    path('livro/<int:livro_id>/', views.detalhes_do_livro, name='detalhes_do_livro'),
]