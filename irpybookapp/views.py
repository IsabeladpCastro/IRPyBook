from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from .forms import LivroForm, AdicionarLivroForm
from .models import Livro, RegistroLivro, LivroAdicionado, AtividadeUsuario
import requests, re

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f'Sucesso ao entrar com {username}')
            return redirect('home')
        else:
            messages.error(request, 'Nome de usuario ou senha incorretos.')
            print(f'Falha ao entrar com o {username}')
            
    return render(request, 'login.html')
        
def mainPage(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro Bem-Sucedido')
            return redirect('home')
        else:
            messages.error(request, 'Erro no Registro')
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})

@login_required
def registerBook(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save()
            
            RegistroLivro.objects.create(usuario=request.user, livro=livro)
            
            print(f'Livro registrado: {livro.titulo}, {livro.autor}, {livro.data}')
            messages.success(request, 'Livro registrado com sucesso')
            return redirect('home')
        else:
            messages.error(request, 'Erro no registro do livro')
            print('ta dando erro aqui oia', form.errors)
    else:  
        form = LivroForm()      
        
        
    return render(request, 'registerBook.html', {'form': form})

#Essa função tem o objetivo de pegar os dados da API do google e armazanando na variavel livro
def buscar_livros(titulo, chave_api):
    
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{titulo}&key={chave_api}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        dados_livros = response.json()
        livros = []
        
        if "items" in dados_livros: 
            
            for item in dados_livros["items"]:
                livro_info = {
                    'title': item['volumeInfo']['title'],
                    'authors': item['volumeInfo'].get('authors', []),
                    'thumbnail': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                    'id': item.get('id', ''),
                }
                
                livros.append(livro_info)
        return livros
    return None
     
def book_search(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        print(f"Query: {query}")
        chave_api = 'AIzaSyCKMi0_Tht5Svvm1_A410dSgkb-62gMCew'  
        
        livros = []

        if query and chave_api:
            livros = buscar_livros(query, chave_api)    
        
        if request.method == 'POST':
            form = LivroForm(request.POST)
            if form.is_valid():
                livro = form.save()
                
                RegistroLivro.objects.create(usuario=request.user, livro=livro, favorito=True)
                
                
                print(f'Livro registrado: {livro.titulo}, {livro.autor}, {livro.data}')
                messages.success(request, 'Livro registrado com sucesso')
                return redirect('meusLivros')
            else:
                messages.error(request, 'Erro no registro do livro')
                print('ta dando erro aqui oia', form.errors)
        else:
            form = LivroForm()  
            
        livros_registrados = RegistroLivro.objects.filter(usuario=request.user).values_list("livro", flat=True)
        livros_registrados = Livro.objects.filter(id__in=livros_registrados)
          
        print(f'livros_registrados {livros_registrados}')     
        return render(request, 'home.html', {'books': livros, 'query': query, 'livros_registrados': livros_registrados})
    return render(request, 'home.html', {'books': [], 'query': '', 'livros_registrados': []})


def delete_book(request, livro_id):
    
    livro = get_object_or_404(Livro, pk=livro_id)
    
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluido com sucesso!!')
        return redirect('book_search')
    
    livros = Livro.objects.all()
    
    return render(request, 'home.html', {'livros': livros})

def meusLivros(request):
    #Livros registrados
    livros_registrados = RegistroLivro.objects.filter(usuario=request.user).values_list("livro", flat=True)
    livros_registrados = Livro.objects.filter(pk__in=livros_registrados)

    # Livros adicionados
    livros_adicionados = LivroAdicionado.objects.filter(usuario=request.user).values_list("livro", flat=True)
    livros_adicionados = Livro.objects.filter(pk__in=livros_adicionados)
    
    return render(request, 'meusLivros.html', {'livros_registrados': livros_registrados, 'livros_adicionados': livros_adicionados})

def meuPerfil(request):
    livros_registrados = RegistroLivro.objects.filter(usuario=request.user).count()
    livros_adicionados = LivroAdicionado.objects.filter(usuario=request.user).count()

    return render(request, 'meuPerfil.html', {'livros_registrados': livros_registrados, 'livros_adicionados': livros_adicionados})


def adicionar_livro(request):
    if request.method == 'POST':
        form = AdicionarLivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.save()
            
            LivroAdicionado.objects.create(usuario=request.user, livro=livro)

            messages.success(request, "Livro adicionado com sucesso! Acesse a página de Meus Livros para visualizar os livros favoritados")
            return redirect('meus_livros')
        else:
            messages.error(request, 'Erro ao adicionar o livro. Verifique os dados do formulário.')
    else:
        form = AdicionarLivroForm()

    return render(request, 'adicionar_livro.html', {'form': form})

def fazerLogout(request):
    logout(request) 
    print('Logout realizado com sucesso')
    
    if not request.user.is_authenticated:
        print('Usuário deslogado com sucesso')
    else:
        print('Falha ao deslogar o usuário')
    return redirect('login')

from django.contrib.auth import login as auth_login

def login_social(request):
    
    user = request.user
    auth_login(request, user)
    return redirect('home')

def detalhes_do_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)

    return render(request, 'detalhes_do_livro.html', {'livro': livro})



def registrar_livro(request):

    livro = Livro.objects.create(titulo='Novo Livro', autor='Autor Desconhecido', data=datetime.now())
    
    AtividadeUsuario.objects.create(usuario=request.user, tipo_atividade='registro_livro', livro_relacionado=livro)

    return render(request, 'registro_livro.html', {'livro': livro})