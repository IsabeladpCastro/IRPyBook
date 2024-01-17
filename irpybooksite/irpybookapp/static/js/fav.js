function favoritarLivro(event) {
    event.preventDefault();  // Impede o envio do formulário padrão

    // Obtém o id do livro do atributo data-livro-id
    var livroId = event.target.closest('.favoritar-form').dataset.livroId;

    // Envia uma solicitação AJAX para favoritar o livro
    fetch('{% url "favoritar_livro" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),  // Função para obter o token CSRF
        },
        body: 'livro_id=' + livroId,
    })
    .then(response => response.json())
    .then(data => {
        // Atualize a interface do usuário com os dados recebidos
        // Neste exemplo, você pode atualizar diretamente os contadores em meuPerfil
        document.querySelector('.qtd').innerText = data.livros_registrados;
        document.querySelector('.fav').innerText = data.livros_favoritos;
    })
    .catch(error => console.error('Erro ao favoritar o livro:', error));
}

// Função para obter o valor do token CSRF do cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}