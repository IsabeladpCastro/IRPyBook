from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
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
    return render(request, 'registerBook.html')

def search_books(query):
    api_key = 'AIzaSyCKMi0_Tht5Svvm1_A410dSgkb-62gMCew'
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    
    parametros = {
        'q': query,
        'key': api_key, 
    }
    
    response = request.get(base_url, parametros = parametros)
    data = response.json()
    
    #Processamento de Resultados
    items = data.get('items', [])
    books = []
    
    for item in items:
        book_info = {
            'title': item['volumeInfo']['title'],
            'authors': item['volumeInfo'].get('authors', []),
        }
     