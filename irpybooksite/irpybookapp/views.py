from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import LivroForm
from .models import Livro, RegistroLivro
import requests
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
            else:
                messages.error(request, 'Erro no registro do livro')
                print('ta dando erro aqui oia', form.errors)
        else:
            form = LivroForm()  
            
            livros_favoritos = RegistroLivro.objects.filter(usuario=request.user, favorito=True).count()    
                  
        return render(request, 'home.html', {'books': livros, 'query': query, 'livros': Livro.objects.all(), 'form': form})
    return render(request, 'home.html', {'books': [], 'query': '', 'livros': []})


def delete_book(request, livro_id):
    
    livro = get_object_or_404(Livro, pk=livro_id)
    
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluido com sucesso!!')
        return redirect('book_search')
    
    livros = Livro.objects.all()
    
    return render(request, 'home.html', {'livros': livros})

def meusLivros(request):
    livros_usuario = RegistroLivro.objects.filter(usuario=request.user).values_list("livro",flat=True)
    livros = Livro.objects.filter(pk__in=livros_usuario)
    
    return render(request, 'meusLivros.html', {'livros': livros})

def meuPerfil(request):
    livros_registrados = RegistroLivro.objects.filter(usuario=request.user).count()
    
    
    return render(request, 'meuPerfil.html', {'livros_registrados': livros_registrados})

def favoritar_livros(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)  
    
    if RegistroLivro.objects.filter(usuario=request.user, livro=livro, favorito=True).exists():
        messages.warning(request, 'Livro já está marcado como favorito.')
    else:
        RegistroLivro.objects.create(usuario=request.user, livro=livro, favorito=True)
        messages.success(request, 'Livro marcado como favorito com sucesso.')
    
    return redirect('book_search', query=request.GET.get('query', ''))



def fazerLogout(request):
    logout(request) 
    print('Logout realizado com sucesso')
    
    if not request.user.is_authenticated:
        print('Usuário deslogado com sucesso')
    else:
        print('Falha ao deslogar o usuário')
    return redirect('login')