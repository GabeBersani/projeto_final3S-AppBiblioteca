import requests

URL_BASE = "http://10.135.235.32:5001"


def post_livro(titulo, autor, isbn, resumo):
    dados = {
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,  # Usando 'isbn' minúsculo para consistência
        "resumo": resumo
    }
    try:
        resposta = requests.post(f"{URL_BASE}/novo_livro", json=dados)
        return resposta.status_code == 201
    except Exception as e:
        print(f"Erro ao cadastrar livro: {e}")
        return False

def get_livros():
    try:
        resposta = requests.get(f"{URL_BASE}/livros")
        if resposta.status_code == 200:
            return resposta.json()
    except Exception as e:
        print(f"Erro ao obter livros: {e}")
    return []

def editar_livro(id_livro, titulo=None, autor=None, isbn=None, resumo=None): # Renomeada para editar_livro
    dados = {}
    if titulo is not None:
        dados['titulo'] = titulo
    if autor is not None:
        dados['autor'] = autor
    if isbn is not None:
        dados['isbn'] = isbn  # Usando 'isbn' minúsculo para consistência
    if resumo is not None:
        dados['resumo'] = resumo

    try:
        resposta = requests.put(f"{URL_BASE}/editar_livro/{id_livro}", json=dados) # Rota alterada
        return resposta.status_code == 200
    except Exception as e:
        print(f"Erro ao editar livro: {e}")
        return False

def status_livros():
    try:
        resposta = requests.get(f"{URL_BASE}/livro_status")
        if resposta.status_code == 200:
            return resposta.json()
    except Exception as e:
        print(f"Erro ao obter status dos livros: {e}")
    return {}

# USUÁRIOS
def post_usuarios(nome, cpf, endereco):
    # try:
        dados = {
            "nome": nome,
            "cpf": cpf, # Usando 'cpf' minúsculo para consistência
            "endereco": endereco
        }
        resposta = requests.post(f"{URL_BASE}/novo_usuario", json=dados)

        return resposta.json()
    # except Exception as e:
    #     print(f"Erro ao cadastrar usuário: {e}")
    #     return {
    #         "status": False,
    #         "erro": e
    #     }

# print(post_usuarios("Lucas", "1111111111", "rua111"))

def get_usuarios():
    try:
        resposta = requests.get(f"{URL_BASE}/usuarios")
        if resposta.status_code == 200:
            return resposta.json()
    except Exception as e:
        print(f"Erro ao obter usuários: {e}")
    return []

def editar_usuario(id_usuario, nome=None, cpf=None, endereco=None): # Renomeada para editar_usuario
    dados = {}
    if nome is not None:
        dados['nome'] = nome
    if cpf is not None:
        dados['cpf'] = cpf # Usando 'cpf' minúsculo para consistência
    if endereco is not None:
        dados['endereco'] = endereco
    try:
        resposta = requests.put(f"{URL_BASE}/editar_usuario/{id_usuario}", json=dados) # Rota alterada
        return resposta.status_code == 200
    except Exception as e:
        print(f"Erro ao editar usuário: {e}")
        return False

# EMPRÉSTIMOS
def devolver_livro(id_livro):
    dados = {
        "id_livro": id_livro
    }
    try:
        resposta = requests.post(f"{URL_BASE}/devolver_livro", json=dados)
        return resposta.status_code == 201
    except Exception as e:
        print(f"Erro ao cadastrar empréstimo: {e}")
        return False
def post_emprestimos(id_livro, id_usuario):
    dados = {
        "id_livro": int(id_livro),
        "id_usuario": int(id_usuario)
    }
    try:
        resposta = requests.post(f"{URL_BASE}/realizar_emprestimo", json=dados)
        return resposta.status_code == 201
    except Exception as e:
        print(f"Erro ao cadastrar empréstimo: {e}")
        return False

def get_emprestimos():
    try:
        resposta = requests.get(f"{URL_BASE}/emprestimos")
        if resposta.status_code == 200:
            return resposta.json()
    except Exception as e:
        print(f"Erro ao obter empréstimos: {e}")
    return []