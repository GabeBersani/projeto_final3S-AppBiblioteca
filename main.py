import flet as ft
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
from flet.core.types import CrossAxisAlignment
from flet.utils import which

from api import cadastrar_livros_novos
from funcao import *


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    livros = []


    def salvar_livro(e):
        if titulo.value == "" or autor.value == "" or ISBN.value == "" or resumo.value == "":
            resposta = post_livro(titulo.value, autor.value, ISBN.value, resumo.value)
            if "erro" in resposta:
                msg_erro.open = True
            else:
                titulo.value = autor.value = ISBN.value = resumo.value = ""
                msg_sucesso.open = True
        else:
            msg_erro.open = True
        page.update()

    def salvar_usuario(e):
        if nome.value == "" or CPF.value == "" or endereco.value == "":
            resposta = post_usuarios(nome.value, CPF.value, endereco.value)
            if "erro" in resposta:
                msg_erro.open = True
            else:
                nome.value = CPF.value = endereco.value = ""
                msg_sucesso.open = True
        else:
            msg_erro.open = True
        page.update()

    def salvar_emprestimo(e):
        if (data_devolucao.value == "" or data_emprestimo.value == "" or livro_emprestado.value == "" or usuario_emprestado.value
                == "" or id_usuario.value == "" or id_livro.value == ""):
            resposta = post_emprestimos(data_emprestimo.value, data_devolucao.value, livro_emprestado.value, usuario_emprestado.value, id_usuario.value, id_livro.value)

            if "erro" in resposta:
                msg_erro.open = True
            else:
                data_emprestimo.value = data_devolucao.value = livro_emprestado.value = usuario_emprestado.value = id_usuario.value = id_livro.value = ""
                msg_sucesso.open = True
        else:
            msg_erro.open = True
        page.update()


    def exibir_lista_livros(e):
        lv_livro.controls.clear()
        livros = get_livros()
        for l in livros:
            lv_livro.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(l["titulo"]),
                    subtitle=ft.Text(l["autor"]),
                    trailing=ft.PopupMenuButton(
                        items=[ft.PopupMenuItem(text="Detalhes")],
                        on_select=lambda _, liv=l: ver_detalhes(liv["titulo"], liv["autor"], liv["ISBN"], liv["resumo"]),
                    ),
                )
            )
        page.update()

    def ver_detalhes(titulo_, autor_, ISBN_, resumo_):
        txt.value = f"Título: {titulo_}\nAutor: {autor_}\nISBN: {ISBN_}\nResumo: {resumo_}"
        page.go("/listar_detalhes")

    def exibir_lista_usuario(e):
        usu_usuarios.controls.clear()
        usuarios = get_usuarios()
        for u in usuarios:
            usu_usuarios.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(u["Nome"]),
                    trailing=ft.PopupMenuButton(
                        items=[ft.PopupMenuItem(text="Detalhes")],
                        on_select=lambda _, usu=u: ver_detalhes_usu(usu["Nome"], usu["CPF"], usu["Endereço"]),
                    ),
                )
            )
        page.update()

    def ver_detalhes_usu(nome_, CPF_, endereco_):
        txt_usu.value = f"Nome: {nome_}\nCPF: {CPF_}\nEndereço: {endereco_}"
        page.go("/listar_detalhes_usu")

    def exibir_lista_emprestimo(e):
        emp_emprestimos.controls.clear()
        emprestimos = get_emprestimos()
        for emp in emprestimos:
            emp_emprestimos.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(emp["data_emprestimo"]),
                    subtitle=ft.Text(emp["data_devolucao"]),
                    trailing=ft.PopupMenuButton(
                        items=[ft.PopupMenuItem(text="Detalhes")],
                        on_select=lambda _, e=emp: ver_detalhes_empres(
                            e["data_emprestimo"], e["data_devolucao"],
                            e["livro_emprestado"], e["usuario_emprestado"],
                            e["id_usuario"], e["id_livro"]
                        ),
                    ),
                )
            )
        page.update()

    def ver_detalhes_empres(data_emp, data_dev, livro, usuario, id_usu, id_liv):
        txt_empres.value = (
            f"Data Empréstimo: {data_emp}\n"
            f"Data Devolução: {data_dev}\n"
            f"Livro: {livro}\nUsuário: {usuario}\n"
            f"ID Usuário: {id_usu}\nID Livro: {id_liv}"
        )
        page.go("/listar_detalhes_emprestimo")

    def gerencia_rota(e):
        rota = page.route
        page.views.clear()

        page.views.append(
            View(
                "/",
                [
                        ft.Image(src="logo (2).png"),
                    ElevatedButton("Usuarios", on_click=lambda _: page.go("/usuario"), width=150, color=ft.CupertinoColors.SYSTEM_PURPLE),
                    ElevatedButton("Livros", on_click=lambda _: page.go("/livro"), color=ft.CupertinoColors.SYSTEM_PURPLE, width=150),
                    ElevatedButton("Emprestimos", on_click=lambda _: page.go("/emprestimos"),color=ft.CupertinoColors.SYSTEM_PURPLE, width=150),
                ],
                bgcolor=Colors. PURPLE_900,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/usuario":
            page.views.append(
                View(
                    "/usuario",
                    [
                        ft.Image(src="usu.png"),
                        AppBar(title=Text(""), bgcolor=Colors.YELLOW_700),
                        ElevatedButton(text="Cadastro de usuario", on_click=lambda _: page.go("/cadastro_usu"),
                                       width=150, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton(text="Visualizar usuario", on_click=lambda _: page.go("/lista_usu"),
                                       width=150, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton(text="Editar usuario", on_click=lambda _: page.go("/editar_usu"),
                                       width=150, color=ft.CupertinoColors.SYSTEM_PURPLE)

                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        page.update()

        if page.route == "/livro":
            page.views.append(
                View(
                    "/livro",
                    [
                        ft.Image(src="liv.png"),
                        AppBar(title=Text(""), bgcolor=Colors.YELLOW_700),
                        ElevatedButton(text="Cadastro de livro", on_click=lambda _: page.go("/cadastro_liv"),
                                       width=150, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton(text="Visualizar livros", on_click=lambda _: page.go("/lista_liv"),
                                       width=150, color=ft.CupertinoColors.SYSTEM_PURPLE),
                        ElevatedButton(text="Editar livro", on_click=lambda _: page.go("/editar_liv"),
                                       width=150, color=ft.CupertinoColors.SYSTEM_PURPLE)
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        page.update()

        if page.route == "/emprestimos":
            page.views.append(
                View(
                    "/emprestimos",
                    [
                        ft.Image(src="empres.png"),
                        AppBar(title=Text(""), bgcolor=Colors.YELLOW_700),
                        ElevatedButton(text="Realizar emprestimo", on_click=lambda _: page.go("/emprestimo"),
                                       color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                        ElevatedButton(text="Visualizar emprestimo", on_click=lambda _: page.go("/lista_emprestimo"),
                                       color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ],
                    bgcolor=Colors.PURPLE_900,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        page.update()

        if rota == "/cadastro_liv":
            page.views.append(View(rota, [AppBar(title=Text("Cadastro de livro"), bgcolor=Colors.YELLOW_700),                                          titulo,
                                          autor,
                                          ISBN,
                                          resumo,
                                          ElevatedButton("Salvar", on_click=salvar_livro,
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375
                                                         ),
                                          ElevatedButton(text="Voltar", on_click=lambda _: page.go("/livro"),
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375)

                                          ],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        if rota == "/cadastro_usu":
            page.views.append(View(rota, [AppBar(title=Text("Cadastro de usuario"), bgcolor=Colors.YELLOW_700),
                                          nome,
                                          CPF, endereco,
                                          ElevatedButton("Salvar", on_click=salvar_usuario,
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375
                                                         ),
                                          ElevatedButton(text="Voltar", on_click=lambda _: page.go("/usuario"),
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375)
                                          ],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        if rota == "/emprestimo":
            page.views.append(View(rota, [AppBar(title=Text("Realizar emprestimos"), bgcolor=Colors.YELLOW_700),
                                          data_emprestimo,
                                          data_devolucao,
                                          livro_emprestado,
                                          usuario_emprestado,
                                          id_usuario, id_livro,
                                          ElevatedButton("Salvar", on_click=salvar_emprestimo,
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375),
                                          ElevatedButton(text="Voltar", on_click=lambda _: page.go("/emprestimos"),
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375)
                                          ],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )


        if rota == "/lista_liv":
            exibir_lista_livros(e)
            page.views.append(View(rota, [
                AppBar(title=Text("Lista de livros"), bgcolor=Colors.YELLOW_700),
                lv_livro,
                ElevatedButton(text="Voltar", on_click=lambda _: page.go("/livro"),
                               color=ft.CupertinoColors.SYSTEM_PURPLE, width=375)
            ],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        if rota == "/listar_detalhes":
            page.views.append(View(rota, [AppBar(title=Text(""), bgcolor=Colors.YELLOW_700),
                                          txt],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        if rota == "/lista_usu":
            exibir_lista_usuario(e)
            page.views.append(View(rota, [AppBar(title=Text("Lista de usuarios"), bgcolor=Colors.YELLOW_700),
                                          usu_usuarios,
                                          ElevatedButton(text="Voltar", on_click=lambda _: page.go("/usuario"),
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375)
                                          ],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        if rota == "/listar_detalhes_usu":
            page.views.append(View(rota, [AppBar(title=Text(""), bgcolor=Colors.YELLOW_700),
                                          txt_usu],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        if rota == "/lista_emprestimo":
            exibir_lista_emprestimo(e)
            page.views.append(View(rota, [AppBar(title=Text("Lista de emprestimos"), bgcolor=Colors.YELLOW_700),
                                          emp_emprestimos,
                                          ElevatedButton(text="Voltar", on_click=lambda _: page.go("/emprestimos"),
                                                         color=ft.CupertinoColors.SYSTEM_PURPLE, width=375)
                                          ],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        if rota == "/listar_detalhes_emprestimo":
            page.views.append(View(rota, [AppBar(title=Text(""), bgcolor=Colors.YELLOW_700),
                                          txt_empres],
                                   bgcolor=Colors.PURPLE_900,
                                   horizontal_alignment=CrossAxisAlignment.CENTER,
                                   )
                              )

        page.update()

    def voltar(e):
        page.views.pop()
        page.go(page.views[-1].route)

    msg_sucesso = ft.SnackBar(content=Text("Cadastro realizado com sucesso!"), bgcolor=Colors.GREEN)
    msg_erro = ft.SnackBar(content=Text("Preencha todos os campos!"), bgcolor=Colors.RED)
    page.overlay.append(msg_sucesso)
    page.overlay.append(msg_erro)



    nome = ft.TextField(label="Nome")
    CPF = ft.TextField(label="CPF")
    endereco = ft.TextField(label="Endereço")

    titulo = ft.TextField(label="Título")
    autor = ft.TextField(label="Autor")
    ISBN = ft.TextField(label="ISBN")
    resumo = ft.TextField(label="Resumo")

    data_emprestimo = ft.TextField(label="Data Empréstimo")
    data_devolucao = ft.TextField(label="Data Devolução")
    livro_emprestado = ft.TextField(label="Livro Emprestado")
    usuario_emprestado = ft.TextField(label="Usuário Emprestado")
    id_usuario = ft.TextField(label="ID Usuário")
    id_livro = ft.TextField(label="ID Livro")

    txt = ft.Text()
    txt_usu = ft.Text()
    txt_empres = ft.Text()

    lv_livro = ft.ListView(height=500, spacing=1, divider_thickness=1)
    usu_usuarios = ft.ListView(height=500, spacing=1, divider_thickness=1)
    emp_emprestimos = ft.ListView(height=500, spacing=1, divider_thickness=1)

    page.on_route_change = gerencia_rota
    page.on_view_pop = voltar
    page.go(page.route)


ft.app(main)