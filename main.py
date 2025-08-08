import flet as ft
from flet import (
    AppBar, Text, View, ElevatedButton, TextField, ListView,
    ListTile, Icon, PopupMenuButton, PopupMenuItem, Image, Dropdown
)
from flet.core.colors import Colors
from flet.core.dropdown import Option
from flet.core.types import CrossAxisAlignment

from funcao import (
    post_livro, get_livros, editar_livro,
    post_usuarios, get_usuarios, editar_usuario,
    post_emprestimos, get_emprestimos, status_livros
)


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667


    # carregar dropdowns
    def carregar_livros_dropdown():
        livros_data = get_livros()
        dado = []

        for livro in livros_data['livros']:
            dado.append(Option(
                key=str(livro['id_livro']),
                text=f"{livro['titulo']} (ID: {livro['id_livro']})"
            ))
        dd_livro.options = dado
        page.update()

    def carregar_usuarios_dropdown():
        usuarios_data = get_usuarios()
        dado = []
        for usuario in usuarios_data['usuarios']:
            dado.append(Option(
                key=str(usuario['id_usuario']),
                text=f"{usuario['nome']} (ID: {usuario['id_usuario']})"
            ))
        dd_usuario.options = dado
        page.update()


    #salvar
    def salvar_livro(e):
        if titulo.value.strip() and autor.value.strip() and ISBN.value.strip() and resumo.value.strip():
            sucesso = post_livro(titulo.value.strip(), autor.value.strip(), ISBN.value.strip(), resumo.value.strip())
            if sucesso:
                titulo.value = autor.value = ISBN.value = resumo.value = ""
                msg_sucesso.open = True
                exibir_lista_livros(None)
            else:
                msg_erro.content = Text("Falha ao cadastrar")
                msg_erro.open = True
        else:
            msg_erro.content = Text("Preencha todos os campos!")
            msg_erro.open = True
        page.update()

    def salvar_usuario(e):
        if nome.value.strip() and CPF.value.strip() and endereco.value.strip():
            sucesso = post_usuarios(nome.value.strip(), CPF.value.strip(), endereco.value.strip())
            if sucesso["status"]:
                msg_sucesso.open = True
                page.go("/lista_usu")
            else:
                msg_erro.content = Text(f"{sucesso['erro']}")
                msg_erro.open = True
        else:
            msg_erro.content = Text("Preencha todos os campos!")
            msg_erro.open = True
        page.update()

    def salvar_emprestimo(e):
        # Pega os IDs selecionados dos Dropdowns
        selected_livro_id = dd_livro.value
        selected_usuario_id = dd_usuario.value

        if selected_livro_id and selected_usuario_id:  # ver se os Dropdowns têm valor
            sucesso = post_emprestimos(
                selected_livro_id,
                selected_usuario_id)
            if sucesso:
                data_emprestimo.value = data_devolucao.value = ""
                dd_livro.value = None  # limoa a seleção do drop
                dd_usuario.value = None  # limpa a seleção do drop
                msg_sucesso.open = True
                page.go("/lista_empres")
            else:
                msg_erro.content = Text("Falha ao cadastrar")
                msg_erro.open = True
        else:
            msg_erro.content = Text("Preencha todos os campos!")
            msg_erro.open = True
        page.update()


    def salvar_editar_livro(e):
        nonlocal editar_livro_id
        if editar_livro_id is None:
            msg_erro.content = Text("Nenhum livro selecionado para editar")
            msg_erro.open = True
            page.update()
            return
        if edit_titulo.value.strip() and edit_autor.value.strip() and edit_ISBN.value.strip() and edit_resumo.value.strip():
            sucesso = editar_livro(
                editar_livro_id,
                titulo=edit_titulo.value.strip(),
                autor=edit_autor.value.strip(),
                isbn=edit_ISBN.value.strip(),
                resumo=edit_resumo.value.strip()
            )
            if sucesso:
                msg_sucesso.open = True
                editar_livro_id = None
                exibir_lista_livros(None)
                page.go("/lista_liv")
            else:
                msg_erro.content = Text("Falha ao editar livro.")
                msg_erro.open = True
        else:
            msg_erro.content = Text("Preencha todos os campos!")
            msg_erro.open = True
        page.update()

    def salvar_editar_usuario(e):
        nonlocal editar_usu_id
        if editar_usu_id is None:
            msg_erro.content = Text("Nenhum usuário selecionado para editar")
            msg_erro.open = True
            page.update()
            return
        if edit_nome.value.strip() and edit_CPF.value.strip() and edit_endereco.value.strip():
            sucesso = editar_usuario(
                editar_usu_id,
                nome=edit_nome.value.strip(),
                cpf=edit_CPF.value.strip(),
                endereco=edit_endereco.value.strip()
            )
            if sucesso:
                msg_sucesso.open = True
                editar_usu_id = None
                exibir_lista_usuario(e)
                page.go("/lista_usu")
            else:
                msg_erro.content = Text("Falha ao editar usuário")
                msg_erro.open = True
        else:
            msg_erro.content = Text("Preencha todos os campos!")
            msg_erro.open = True
        page.update()

    def exibir_lista_livros(e):
        lv_livro.controls.clear()
        livros = get_livros()
        if not livros or 'livros' not in livros or not livros['livros']:
            lv_livro.controls.append(Text("livro nao encontrado"))
        else:
            for l in livros['livros']:
                lv_livro.controls.append(
                    ListTile(
                        leading=Icon(ft.Icons.BOOK),
                        title=Text(l["titulo"]),
                        subtitle=Text(f"Autor: {l['autor']}"),
                        trailing=PopupMenuButton(
                            items=[
                                PopupMenuItem(text="Detalhes", on_click=lambda _, liv=l: ver_detalhes(liv)),
                                PopupMenuItem(text="Editar", on_click=lambda _, liv=l: iniciar_edicao_livro(liv)),
                            ]
                        )
                    )
                )
        page.update()

    def iniciar_edicao_livro(livro):
        nonlocal editar_livro_id
        editar_livro_id = livro.get("id_livro")
        edit_titulo.value = livro["titulo"]
        edit_autor.value = livro["autor"]
        edit_ISBN.value = str(livro.get("isbn", ""))
        edit_resumo.value = livro["resumo"]
        page.go("/editar_livro")
        page.update()

    def ver_detalhes(livro):
        titulo_ = livro.get("titulo")
        autor_ = livro.get("autor")
        ISBN_ = livro.get("isbn")
        resumo_ = livro.get("resumo")
        txt.value = f"Título: {titulo_}\nAutor: {autor_}\nISBN: {ISBN_}\nResumo: {resumo_}"
        page.go("/listar_detalhes")
        page.update()

    def exibir_lista_usuario(e):
        usu_usuarios.controls.clear()
        usuarios = get_usuarios()
        if not usuarios or 'usuarios' not in usuarios or not usuarios['usuarios']:
            usu_usuarios.controls.append(Text("Nenhum usuário encontrado."))
        else:
            for u in usuarios['usuarios']:
                usu_usuarios.controls.append(
                    ListTile(
                        leading=Icon(ft.Icons.PERSON),
                        title=Text(u["nome"]),
                        subtitle=Text(f"CPF: {u.get('cpf', '')}"),
                        trailing=PopupMenuButton(
                            items=[
                                PopupMenuItem(text="Detalhes", on_click=lambda _, usu=u: ver_detalhes_usu(usu)),
                                PopupMenuItem(text="Editar", on_click=lambda _, usu=u: iniciar_edicao_usuario(usu)),

                            ]
                        )
                    )
                )
        page.update()

    def iniciar_edicao_usuario(usuario):
        nonlocal editar_usu_id
        editar_usu_id = usuario.get("id_usuario")
        edit_nome.value = usuario["nome"]
        edit_CPF.value = usuario.get("cpf", "")
        edit_endereco.value = usuario["endereco"]
        page.go("/editar_usuario")
        page.update()

    def ver_detalhes_usu(usuario):
        nome_ = usuario.get("nome")
        CPF_ = usuario.get("cpf")
        endereco_ = usuario.get("endereco")
        txt_usu.value = f"Nome: {nome_}\nCPF: {CPF_}\nEndereço: {endereco_}"
        page.go("/listar_detalhes_usu")
        page.update()

    def exibir_lista_emprestimo(e):
        emp_emprestimos.controls.clear()  # limpaa a lista antes de adicionar
        emprestimos = get_emprestimos()
        if not emprestimos or 'emprestimos' not in emprestimos or not emprestimos['emprestimos']:
            emp_emprestimos.controls.append(Text("Nenhum empréstimo encontrado."))
        else:
            for emp in emprestimos['emprestimos']:
                emp_emprestimos.controls.append(
                    ListTile(
                        leading=Icon(ft.Icons.BOOK),
                        title=Text(f"Empréstimo ID: {emp.get('id_emprestimo', '')}"),
                        subtitle=Text(
                            f"Data: {emp.get('data_de_emprestimo', '')} - Devolução: {emp.get('data_de_devolucao', '')}\nUsuário ID: {emp.get('id_usuario', '')} - Livro ID: {emp.get('id_livro', '')}"),
                    )
                )
        page.update()

    def exibir_status_livros(e):
        txt_status.value = ""
        status = status_livros()
        if not status:
            txt_status.value = "Erro ao obter o status"
            page.update()
            return

        livros_emprestados = status.get("livros_emprestados", [])
        livros_disponiveis = status.get("livros_disponiveis", [])

        status_text = f"Livros Emprestados ({len(livros_emprestados)}):\n"
        if livros_emprestados:
            for l in livros_emprestados:
                status_text += f"- {l.get('titulo')} (ID: {l.get('id_livro')})\n"
        else:
            status_text += "Nenhum livro emprestado\n"

        status_text += f"\nLivros Disponíveis ({len(livros_disponiveis)}):\n"
        if livros_disponiveis:
            for l in livros_disponiveis:
                status_text += f" {l.get('titulo')} ID: {l.get('id_livro')}\n"
        else:
            status_text += "Nenhum livro disponível\n"

        txt_status.value = status_text
        page.go("/livro_status")
        page.update()

    # Gerenciamento das rotas
    def gerencia_rota(e):
        rota = page.route
        page.views.clear()

        page.views.append(
            View(
                "/",
                [
                    Image(src="logo (2).png"),
                    ElevatedButton("Usuários", on_click=lambda _: page.go("/usuario"), width=200,
                                   color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ElevatedButton("Livros", on_click=lambda _: page.go("/livro"), width=200,
                                   color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ElevatedButton("Empréstimos", on_click=lambda _: page.go("/emprestimos"), width=200,
                                   color=ft.CupertinoColors.SYSTEM_PURPLE),
                ],
                bgcolor=Colors.PURPLE_900,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        if rota == "/usuario":
            page.views.append(
                View(
                    "/usuario",
                    [
                        Image(src="usu.png"),
                        AppBar(title=Text("Usuários"), bgcolor=Colors.YELLOW_700),
                        ElevatedButton("Cadastro de usuário", on_click=lambda _: page.go("/cadastro_usu"),
                                       width=200, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton("Visualizar usuários", on_click=lambda _: page.go("/lista_usu"),
                                       width=200, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/livro":
            page.views.append(
                View(
                    "/livro",
                    [
                        Image(src="liv.png"),
                        AppBar(title=Text("Livros"), bgcolor=Colors.YELLOW_700),
                        ElevatedButton("Cadastro de livro", on_click=lambda _: page.go("/cadastro_liv"),
                                       width=200, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton("Visualizar livros", on_click=lambda _: page.go("/lista_liv"),
                                       width=200, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton("Status dos Livros", on_click=exibir_status_livros,
                                       width=200, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/emprestimos":
            page.views.append(
                View(
                    "/emprestimos",
                    [
                        Image(src="empres.png"),
                        AppBar(title=Text("Empréstimos"), bgcolor=Colors.YELLOW_700),
                        ElevatedButton("Realizar empréstimo", on_click=lambda _: page.go("/cadastro_empres"),
                                       width=200, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton("Visualizar empréstimos", on_click=lambda _: page.go("/lista_empres"),
                                       width=200, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/cadastro_liv":
            page.views.append(
                View(
                    "/cadastro_liv",
                    [
                        AppBar(title=Text("Cadastro de Livro"), bgcolor=Colors.YELLOW_700),
                        titulo,
                        autor,
                        ISBN,
                        resumo,
                        ElevatedButton("Salvar", on_click=salvar_livro,width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/lista_liv":
            page.views.append(
                View(
                    "/lista_liv",
                    [
                        AppBar(title=Text("Lista de Livros"), bgcolor=Colors.YELLOW_700),
                        lv_livro,
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
            exibir_lista_livros(None)  # carwega a lista ao entrar na rota

        if rota == "/editar_livro":
            page.views.append(
                View(
                    "/editar_livro",
                    [
                        AppBar(title=Text("Editar Livro"), bgcolor=Colors.YELLOW_700),
                        edit_titulo,
                        edit_autor,
                        edit_ISBN,
                        edit_resumo,
                        ElevatedButton("Salvar Alterações", on_click=salvar_editar_livro, width=375, color=ft.CupertinoColors.SYSTEM_PURPLE ),
                        ElevatedButton("Voltar", on_click=lambda e: page.go("/lista_liv"), width=375, color=ft.CupertinoColors.SYSTEM_PURPLE ),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/cadastro_usu":
            page.views.append(
                View(
                    "/cadastro_usu",
                    [
                        AppBar(title=Text("Cadastro de Usuário"), bgcolor=Colors.YELLOW_700),
                        nome,
                        CPF,
                        endereco,
                        ElevatedButton("Salvar", on_click=salvar_usuario, width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/lista_usu":
            page.views.append(
                View(
                    "/lista_usu",
                    [
                        AppBar(title=Text("Lista de Usuários"), bgcolor=Colors.YELLOW_700),
                        usu_usuarios,
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
            exibir_lista_usuario(e)  # carrega a lista ao entrar na rota

        if rota == "/editar_usuario":
            page.views.append(
                View(
                    "/editar_usuario",
                    [
                        AppBar(title=Text("Editar Usuário"), bgcolor=Colors.YELLOW_700),
                        edit_nome,
                        edit_CPF,
                        edit_endereco,
                        ElevatedButton("Salvar Alterações", on_click=salvar_editar_usuario, width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton("Voltar", on_click=lambda e: page.go("/lista_usu"), width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/cadastro_empres":
            carregar_livros_dropdown()
            carregar_usuarios_dropdown()
            page.views.append(
                View(
                    "/cadastro_empres",
                    [
                        AppBar(title=Text("Cadastro de Empréstimo"), bgcolor=Colors.YELLOW_700),
                        dd_livro,  # Dropdown liv
                        dd_usuario,  # Dropdown usu

                        ElevatedButton("Realizar Empréstimo", on_click=salvar_emprestimo, width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/lista_empres":
            page.views.append(
                View(
                    "/lista_empres",
                    [
                        AppBar(title=Text("Lista de Empréstimos"), bgcolor=Colors.YELLOW_700),
                        emp_emprestimos,
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
            exibir_lista_emprestimo(None)  # Carrega a lista ao entrar na rota

        if rota == "/listar_detalhes":
            page.views.append(
                View(
                    "/listar_detalhes",
                    [
                        AppBar(title=Text("Detalhes do Livro"), bgcolor=Colors.YELLOW_700),
                        txt,
                        ElevatedButton("Voltar", on_click=lambda e: page.go("/lista_liv"), width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/listar_detalhes_usu":
            page.views.append(
                View(
                    "/listar_detalhes_usu",
                    [
                        AppBar(title=Text("Detalhes do Usuário"), bgcolor=Colors.YELLOW_700),
                        txt_usu,
                        ElevatedButton("Voltar", on_click=lambda e: page.go("/lista_usu"), width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if rota == "/listar_detalhes_emprestimo":
            page.views.append(
                View(
                    "/listar_detalhes_emprestimo",
                    [
                        AppBar(title=Text("Detalhes do Empréstimo"), bgcolor=Colors.YELLOW_700),
                        txt_empres,
                        ElevatedButton("Voltar", on_click=lambda e: page.go("/lista_empres"), width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        # status do livro
        if rota == "/livro_status":
            page.views.append(
                View(
                    "/livro_status",
                    [
                        AppBar(title=Text("Status dos Livros"), bgcolor=Colors.YELLOW_700),
                        Text(value=txt_status.value, selectable=True),
                        ElevatedButton("Voltar", on_click=lambda e: page.go("/livro"), width=375, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        page.update()


    # cadastrp do livro
    titulo = TextField(label="Título")
    autor = TextField(label="Autor")
    ISBN = TextField(label="ISBN", keyboard_type=ft.KeyboardType.NUMBER)
    resumo = TextField(label="Resumo")

    # cadastro de usuario
    nome = TextField(label="Nome")
    CPF = TextField(label="CPF", hint_text="Somente números (11 dígitos)",
                    input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
                    max_length=11)
    endereco = TextField(label="Endereço")

    # emprstimo
    data_emprestimo = TextField(label="Data Empréstimo", hint_text="Ex: 27/10/2007")
    data_devolucao = TextField(label="Data Devolução", hint_text="Ex: 27/10/2007")
    # Dropdowns para seleção de livro e usuário
    # livro
    dd_livro = Dropdown(
        label="Selecione o Livro",
        options=[],
        expand=True
    )
    # usuario q vai pegar o livro
    dd_usuario = Dropdown(
        label="Selecione o Usuário",
        options=[],
        expand=True
    )


    edit_titulo = TextField(label="Título")
    edit_autor = TextField(label="Autor")
    edit_ISBN = TextField(label="ISBN", keyboard_type=ft.KeyboardType.NUMBER)
    edit_resumo = TextField(label="Resumo")

    # Campos edição usuários
    edit_nome = TextField(label="Nome")
    edit_CPF = TextField(label="CPF", hint_text="Somente números (11 dígitos)",
                         input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
                         max_length=11)
    edit_endereco = TextField(label="Endereço")


    txt = Text()
    txt_usu = Text()
    txt_empres = Text()
    txt_status = Text(selectable=True)

    # o divider_thickness espessura de um objeto que serve para separar ou dividir duas coisas
    lv_livro = ListView(height=400, spacing=1, divider_thickness=1, expand=True)
    usu_usuarios = ListView(height=400, spacing=1, divider_thickness=1, expand=True)
    emp_emprestimos = ListView(height=400, spacing=1, divider_thickness=1, expand=True)


    msg_sucesso = ft.SnackBar(content=Text("cadastro realizado com sucesso!"), bgcolor=Colors.GREEN)
    msg_erro = ft.SnackBar(content=Text("Erro, verifique os dados!"), bgcolor=Colors.RED)
    page.overlay.append(msg_sucesso)
    page.overlay.append(msg_erro)

    # variavel para edi
    editar_livro_id = None
    editar_usu_id = None

    page.on_route_change = gerencia_rota
    page.on_view_pop = lambda e: page.go(page.route)
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)