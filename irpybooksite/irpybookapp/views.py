from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import LivroForm
from .models import Livro
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

def registerBook(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save()
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
        print(f"Query: {query}")  # Adicione esta linha para depurar
        chave_api = 'AIzaSyCKMi0_Tht5Svvm1_A410dSgkb-62gMCew'  # Substitua pela sua chave API
        
        livros = []

        if query and chave_api:
            livros = buscar_livros(query, chave_api)    
        
        if request.method == 'POST':
            form = LivroForm(request.POST)
            if form.is_valid():
                livro = form.save()
                print(f'Livro registrado: {livro.titulo}, {livro.autor}, {livro.data}')
                messages.success(request, 'Livro registrado com sucesso')
            else:
                messages.error(request, 'Erro no registro do livro')
                print('ta dando erro aqui oia', form.errors)
        else:
            form = LivroForm()        
                  
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
    return render(request, 'meusLivros.html')

def meuPerfil(request):
    return render(request, 'meuPerfil.html')