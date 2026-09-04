import json
import os

def tabela():
    arquivos = ["livros.json", "usuarios.json"]

    for arquivo in arquivos:
        if not os.path.exists (arquivo):
            with open (arquivo, "w", encoding = "utf-8") as f:
                json.dump([], f, indent = 3)
            print(f"Arquivo criado: {arquivo}")
        else:
            print(f"Arquivo já existe: {arquivo}")
tabela()

def carregar(arquivo):
    if not os.path.exists(arquivo):
        return []

    try:
        with open(arquivo, "r", encoding = "utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def salvar(arquivo, dados):
    with open(arquivo, "w", encoding = "utf-8") as f:
        json.dump(dados, f, indent = 4, ensure_ascii = False)

def gerar_id(lista):
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1

def cadastrar_livro():
    livros = carregar("livros.json")
    try:
        ano = int(input("Ano: "))
    except ValueError:
        print("Ano inválido.")
        return

    novo_livro = {
        "id": gerar_id(livros),
        "titulo": input("Título: "),
        "autor": input("Autor: "),
        "ano": ano,
        "status": "disponivel"
    }

    livros.append(novo_livro)
    salvar("livros.json", livros)

    print(f"\nLivro cadastrado com sucesso! O ID do livro é: {novo_livro['id']}")

def listar_livros():
    livros = carregar("livros.json")
    if len(livros) == 0:
        print("\nNenhum livro cadastrado.")
        return
    tamanho_pagina = 5

    for i in range(0, len(livros), tamanho_pagina):
        pagina = livros[i:i + tamanho_pagina]
        print("\n=== LIVROS ===")
        for livro in pagina:
            print((f"ID: { livro['id'] } | { livro['titulo'] } - { livro['autor'] } ( { livro['ano'] } ) [ { livro['status'] } ]"))


def remover_livros():
    livros = carregar("livros.json")
    listar_livros()
    try:
        id_livro = int(input("\nDigite o ID do livro para remover: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return
    
    livro_encontrado = next((l for l in livros if l["id"] == id_livro), None)

    if livro_encontrado:
        livros_atualizados = [l for l in livros if l["id"] != id_livro]
        salvar("livros.json", livros_atualizados)
        print("\nLivro removido com sucesso.")
    else:
        print("Livro não encontrado.")
        return

def menu_livros():
    while True:
        print("\n=== MENU DE LIVROS ===")
        print("1 - Cadastrar Livro")
        print("2 - Listar Livros")
        print("3 - Remover Livro")
        print("4 - Buscar livros")
        print("5 - Voltar")

        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                cadastrar_livro()
            case "2":
                listar_livros()
            case "3":
                remover_livros()
            case "4":
                buscar_livros()
            case "5":
                break
            case _:
                print("Opção inválida.")

def cadastrar_usuario():
    usuarios = carregar("usuarios.json")
    nome = input("Nome: ")
    email = input("Email: ")

    for i in usuarios:
        if i["email"].lower() == email.lower():
            print("\nErro: Email já cadastrado.")
            return

    novo_usuario = {
        "id": gerar_id(usuarios),
        "nome": nome,
        "email": email,
        "emprestimos": []
    }
    usuarios.append(novo_usuario)
    salvar("usuarios.json", usuarios)
    
    print(f"\nUsuário cadastrado com sucesso! Seu ID é: {novo_usuario['id']}")

def listar_usuarios():
    usuarios = carregar("usuarios.json")
    if len(usuarios) == 0:
        print("\nNenhum usuário cadastrado.")
        return
    tamanho_pagina = 5
    for i in range(0, len(usuarios), tamanho_pagina):
        pagina = usuarios[i:i + tamanho_pagina]
        print("\n=== Usuários ===")
        for usuario in pagina:
            print(f'ID: { usuario["id"] } | { usuario["nome"] } - { usuario["email"] }')

        if i + tamanho_pagina < len(usuarios):
            continuar = input("\nPressione ENTER para próxima página, X para sair: ")
            if continuar.lower() == "x":
                break 

def remover_usuario():
    usuarios = carregar("usuarios.json")
    listar_usuarios()
    try:
        id_usuario = int(input("Digite ID do usuário para remover: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return

    usuario_encontrado = next((u for u in usuarios if u["id"] == id_usuario), None)

    if not usuario_encontrado:
        print("Usuário não encontrado.")
        return

    if len(usuario_encontrado["emprestimos"]) > 0:
        print("\nErro: Não é possível remover um usuário com empréstimos ativos.")
        return

    usuarios_atualizados = [u for u in usuarios if u["id"] != id_usuario]
    salvar("usuarios.json", usuarios_atualizados)
    print("\nUsuário removido com sucesso.")

def menu_usuarios():
    while True:
        print("\n=== MENU DE USUÁRIOS ===")
        print("1 - Cadastrar Usuário")
        print("2 - Listar Usuários")
        print("3 - Remover Usuário")
        print("4 - Voltar")

        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                cadastrar_usuario()
            case "2":
                listar_usuarios()      
            case "3":
                remover_usuario()
            case "4":
                break
            case _:
                print("Opção inválida.")


def realizar_emprestimo():
    usuarios = carregar("usuarios.json")
    livros = carregar("livros.json")

    print("\n=== REALIZAR EMPRÉSTIMO ===")
    listar_usuarios()
    try:
        id_usuario = int(input("ID do usuário: "))
    except ValueError:
        print("ID inválido")
        return
    usuario = next((u for u in usuarios if u["id"] == id_usuario), None)
    if usuario is None:
        print("Usuário não encontrado.")
        return
    listar_livros()
    try:
        id_livro = int(input("ID do livro: "))
    except ValueError:
        print("ID inválido.")
        return
    livro = next((l for l in livros if l["id"] == id_livro), None)
    if livro is None:
        print("Livro não encontrado.")
        return

    if livro["status"] == "emprestado":
        print("Este livro já está emprestado!")
        return

    livro["status"] = "emprestado"
    usuario["emprestimos"].append(id_livro)

    salvar("livros.json", livros)
    salvar("usuarios.json", usuarios)
    print("\nEmpréstimo realizado com sucesso!")

def realizar_devolucao():
    usuarios = carregar("usuarios.json")
    livros = carregar("livros.json")

    print("\n=== REALIZAR DEVOLUÇÃO ===")
    listar_usuarios()

    try:
        id_usuario = int(input("ID do usuário: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return
    
    usuario = next((u for u in usuarios if u["id"] == id_usuario), None)

    if usuario is None:
        print("\nUsuário não encontrado.")
        return
    
    if len(usuario["emprestimos"]) == 0:
        print("\nEste usuário não possui livros emprestados.")
        return
    
    print("\nLivros emprestados por este usuário:")
    for id_livro in usuario["emprestimos"]:
        livro = next((l for l in livros if l["id"] == id_livro), None)
        print(f"{livro['id']} - {livro['titulo']}")

    try:
        id_livro = int(input("\nID do livro a devolver: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return
    
    if id_livro not in usuario["emprestimos"]:
        print("\nEste livro não está emprestado por este usuário.")
        return
    
    livro = next((l for l in livros if l["id"] == id_livro), None)
    livro["status"] = "disponivel"

    usuario["emprestimos"].remove(id_livro)

    salvar("livros.json", livros)
    salvar("usuarios.json", usuarios)
    print("\nDevolução realizada com sucesso!")

def menu_emprestimos():
    while True:
        print("\n=== MENU DE EMPRÉSTIMOS ===")
        print("1 - Realizar Empréstimo")
        print("2 - Realizar Devolução")
        print("3 - Voltar")

        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                realizar_emprestimo()
            case "2":
                realizar_devolucao()
            case "3":
                break
            case _:
                print("Opção inválida.")

def exibir_resultados(lista):
    if not lista:
        print("\nNenhum resultado encontrado.")
        return

    tamanho = 5

    for i in range(0, len(lista), tamanho):
        pagina = lista[i:i + tamanho]
        print("\n=== RESULTADOS DA BUSCA ===")
        for item in pagina:
            print(f"{item['id']} - {item['titulo']} ({item['ano']})")

def buscar_por_titulo():
    livros = carregar("livros.json")
    termo = input("Digite parte do título: ").lower()

    resultados = []

    for livro in livros:
        if termo in livro["titulo"].lower():
            resultados.append(livro)

    exibir_resultados(resultados)

def buscar_por_status():
    livros = carregar("livros.json")
    status = input("Status (disponivel/emprestado): ").lower()

    if status not in ["disponivel", "emprestado"]:
        print("Status inválido.")
        return

    resultados = []

    for livro in livros:
        if livro["status"] == status:
            resultados.append(livro)

    exibir_resultados(resultados)

def buscar_livros():
    while True:
        print("\n=== BUSCA AVANÇADA ===")
        print("1 - Buscar por Título")
        print("2 - Buscar por Status")
        print("3 - Voltar")

        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                buscar_por_titulo()
            case "2":
                buscar_por_status()
            case "3":
                break
            case _ :
                print("Opção inválida.")
        
def rel_livros_disponiveis():
    livros = carregar("livros.json")
    disponiveis = [l for l in livros if l["status"] == "disponivel"]

    print("\n=== LIVROS DISPONÍVEIS ===")
    for livro in disponiveis:
        print(f"{livro['id']} - {livro['titulo']} ({livro['ano']})")

    print(f"\nTotal: {len(disponiveis)} livros disponíveis.")

def rel_livros_emprestados():
    livros = carregar("livros.json")
    emprestados = [l for l in livros if l["status"] == "emprestado"]

    print("\n=== LIVROS EMPRESTADOS ===")
    for livro in emprestados:
        print(f"{livro['id']} - {livro['titulo']} ({livro['ano']})")

    print(f"\nTotal: {len(emprestados)} livros emprestados.")

def todos_os_livros():
    livros = carregar("livros.json")
    print("\n=== TODOS OS LIVROS ===")
    for livro in livros:
        print(f"{livro['id']} - {livro['titulo']} ({livro['ano']}) [ {livro['status']} ]")
    print(f"\nTotal: {len(livros)} livros cadastrados.")

def menu_relatorios():
    while True:
        print("\n=== MENU DE RELATÓRIOS ===")
        print("1 - Livros Disponíveis")
        print("2 - Livros Emprestados")
        print("3 - Todos os Livros")
        print("4 - Voltar")

        opcao = input("Escolha: ")
        match opcao:
            case "1":
                rel_livros_disponiveis()
            case "2":
                rel_livros_emprestados()
            case "3":
                todos_os_livros()
            case "4":
                break
            case _ :
                print("Opção inválida.")


def menu():
    while True:
        print("\n SISTEMA DE BIBLIOTECA DIGITAL")
        print("="*30)
        print("1 - Gerenciar Livros")
        print("2 - Gerenciar Usuários")
        print("3 - Empréstimos e Devoluções")
        print("4 - Relatórios")
        print("5 - Sair")
        
        opcao = input("\nEscolha uma opção: ")
        match opcao:
            case "1":
                menu_livros()
            case "2":
                menu_usuarios()
            case "3":
                menu_emprestimos()
            case "4":
                menu_relatorios()
            case "5":
                print("Saindo...")
                break
            case _:
                print("Opção Inválida. Tente novamente.")
            
menu()