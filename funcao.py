import requests


def get_livros():
    url = 'http://10.135.232.8:5001/livros'
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        print('Erro ao buscar livros')


def post_livro(titulo, autor, ISBN, resumo):
    url = 'http://10.135.232.8:5001/cadastro_livros'
    livro = {
        'titulo': titulo,
        'autor': autor,
        'ISBN': ISBN,
        'resumo': resumo
    }
    response = requests.post(url, json=livro)
    if response.status_code == 201:
        return response.json()
    else:
        print('Erro ao cadastrar livro')
        return {'erro': response.json()}



def get_usuarios():
    url = 'http://10.135.232.8:5001/usuarios'
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        print('Erro ao buscar usuários')


def post_usuarios(nome, CPF, endereco):
    url = 'http://10.135.232.8:5001/cadastro_usuario'
    usuario = {
        'nome': nome,
        'CPF': CPF,
        'endereco': endereco
    }
    response = requests.post(url, json=usuario)
    if response.status_code == 201:
        return response.json()
    else:
        print('Erro ao cadastrar usuário')
        return {'erro': response.json()}


def get_emprestimos():
    url = 'http://10.135.232.8:5001/emprestimos'
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        print('Erro ao buscar empréstimos')


def post_emprestimos(data_emprestimo, data_devolucao, livro_emprestado, usuario_emprestado, id_usuario, id_livro):
    url = 'http://10.135.232.8:5001/realizacao_emprestimos'
    emprestimo = {
        'data_emprestimo': data_emprestimo,
        'data_devolucao': data_devolucao,
        'livro_emprestado': livro_emprestado,
        'usuario_emprestado': usuario_emprestado,
        'id_usuario': id_usuario,
        'id_livro': id_livro,
    }
    response = requests.post(url, json=emprestimo)
    if response.status_code == 201:
        return response.json()
    else:
        print('Erro ao cadastrar empréstimo')
        return {'erro': response.json()}