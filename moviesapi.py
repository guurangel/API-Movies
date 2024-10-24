# Nome: Gustavo Rangel de Lima Siqueira

# Nome: Heitor Pereira Duarte

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('api_key')
BASE_URL = 'https://api.themoviedb.org/3'


usuarios = {}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def buscar_filme_serie(tipo_busca, nome_busca):
    
    if tipo_busca == 'filme':
        url = f"{BASE_URL}/search/movie"
    elif tipo_busca == 'serie':
        url = f"{BASE_URL}/search/tv"
    
    parametros = {
        'api_key' : API_KEY,
        'query' : nome_busca,
        'language' : 'pt-BR'
    }
    
    resposta = requests.get(url, params=parametros)

    if resposta.status_code == 200:
        dados = resposta.json()
        if dados['results']:
            return dados['results'][0]
    else:
        print(f"Erro ao buscar {tipo_busca}: {resposta.status_code}")
        return None

def exibir_informacoes(resultados, tipo_busca):
    if resultados:
        titulo = resultados['title'] if tipo_busca == "filme" else resultados['name']
        descricao = resultados['overview']
        data_lancamento = resultados['release_date'] if tipo_busca == "filme" else resultados['first_air_date']
        
        clear()
        print("======== [SOBRE O FILME PESQUISADO] ========")
        print(f"\nTítulo: {titulo}")
        print(f"\nData de lançamento: {data_lancamento}")
        print(f"\nDescrição: {descricao}")
        
        input("\nPressione ENTER para continuar...")
    else:
        print(f"\nNenhum(a) {tipo_busca} encontrado com o nome fornecido.")
        time.sleep(5)

def addtopfilmes(email):
    clear()
    print("======== [ADICIONAR TOP 3 FILMES FAVORITOS] ========")
    
    if 'top3_filmes' not in usuarios[email]:
        usuarios[email]['top3_filmes'] = {}
    
    while len(usuarios[email]['top3_filmes']) < 3:
        posicao = len(usuarios[email]['top3_filmes']) + 1
        nome_filme = input(f"\nDigite o nome do filme que deseja adicionar no Top {posicao}: ").strip()
        resultado = buscar_filme_serie('filme', nome_filme)

        if resultado:
            titulo = resultado['title']
            descricao = resultado['overview']
            data_lancamento = resultado['release_date']

            usuarios[email]['top3_filmes'][f'Top {posicao}'] = {
                'titulo': titulo,
                'data_lancamento': data_lancamento,
                'descricao': descricao
            }
            print(f"\nFilme '{titulo}' adicionado ao seu Top {posicao} com sucesso!")
        else:
            print(f"\nNão foi possível encontrar informações para o filme '{nome_filme}'.")
            time.sleep(3)

    print("\nSeu Top 3 filmes favoritos foi cadastrado com sucesso!")
    input("\nPressione ENTER para retornar ao menu...")

def exibirtopfilmes(email):
    if 'top3_filmes' not in usuarios[email] or not usuarios[email]['top3_filmes']:
        print("\nVocê ainda não possui filme no seu Top 3. Retornando ao menu...")
        time.sleep(5)
        return
    
    clear()
    print("======== [SEU TOP 3 FILMES FAVORITOS] ========")
    for posicao in ['Top 1', 'Top 2', 'Top 3']:
        filme = usuarios[email]['top3_filmes'].get(posicao)
        if filme:
            print(f"\n{posicao.capitalize()}: {filme['titulo']}")
            print(f"\nData de lançamento: {filme['data_lancamento']}")
            print(f"\nDescrição: {filme['descricao']}\n")
            print("==============================================")
    input("\nPressione ENTER para retornar ao continuar...")
        
def editartopfilmes(email):
    
    if 'top3_filmes' not in usuarios[email] or not usuarios[email]['top3_filmes']:
        print("\nVocê ainda não possui um Top 3 cadastrado. Por favor, crie um Top 3 antes de editar. Retornando ao menu...")
        time.sleep(3)
        return

    clear()
    print("\n======== [TOP 3 FILMES ATUAIS] ========")
    for posicao in ['Top 1', 'Top 2', 'Top 3']:
        filme = usuarios[email]['top3_filmes'].get(posicao)
        if filme:
            print(f"\n{posicao.capitalize()}: {filme['titulo']}")
            print(f"\nData de lançamento: {filme['data_lancamento']}")
            print(f"\nDescrição: {filme['descricao']}\n")
            print("==============================================")

    while True:
        try:
            posicao = int(input("\nDigite a posição (1, 2 ou 3) que deseja editar: "))
            if posicao in [1, 2, 3]:
                break
            else:
                print("\nPosição inválida! Escolha entre 1, 2 ou 3.")
        except ValueError:
            print("\nEntrada inválida! Digite um número (1, 2 ou 3).")

    novo_filme = input(f"\nDigite o nome do novo filme para o Top {posicao}: ").strip()

    resultado = buscar_filme_serie('filme', novo_filme)

    if resultado:
        usuarios[email]['top3_filmes'][f'Top {posicao}'] = {
            'titulo': resultado['title'],
            'data_lancamento': resultado['release_date'],
            'descricao': resultado['overview']
        }
        print(f"\nTop {posicao} atualizado com sucesso!")
    else:
        print(f"\nNão foi possível adicionar '{novo_filme}' ao Top {posicao}.")

    exibirtopfilmes(email)    

def excluirtopfilmes(email):
    if 'top3_filmes' not in usuarios[email] or not usuarios[email]['top3_filmes']:
        print("\nVocê não possui um Top 3 cadastrado para excluir. Retornando ao menu...")
        time.sleep(5)
        return

    exibirtopfilmes(email)

    while True:
        confirmacao = input("\nTem certeza que deseja excluir o seu Top 3 de filmes? (s/n): ").strip().lower()
        if confirmacao == 's':
            usuarios[email]['top3_filmes'] = {}
            print("\nTop 3 de filmes excluído com sucesso!")
            input("\nPressione ENTER para retornar ao menu...")
            return
        elif confirmacao == 'n':
            print("\nOperação cancelada. Seu Top 3 de filmes permanece intacto.")
            print("\nRetornando ao menu...")
            time.sleep(3)
            return
        else:
            print("\nOpção inválida! Digite novamente")
        
def menutopfilmes(email):
    while True:
        clear()
        print("""
======== [SEU TOP 3 FILMES FAVORITOS] ========

1. CADASTRAR
2. EDITAR    
3. EXCLUIR
4. EXIBIR  
5. VOLTAR AO MENU PRINCIPAL

==============================================
""")
        
        opcao = int(input("Digite a opção desejada: "))
        
        match opcao:
            case 1:
                addtopfilmes(email)
            case 2:
                editartopfilmes(email)
            case 3:
                excluirtopfilmes(email)
            case 4:
                exibirtopfilmes(email)
            case 5:
                print("Voltando ao menu principal...")
                break
            case _:
                print("Opção inválida! Digite um número entre 1 e 5.")

def addtopseries(email):
    clear()
    print("======== [ADICIONAR TOP 3 SÉRIES FAVORITAS] ========")
    
    if 'top3_series' not in usuarios[email]:
        usuarios[email]['top3_series'] = {}
    
    while len(usuarios[email]['top3_series']) < 3:
        posicao = len(usuarios[email]['top3_series']) + 1
        nome_serie = input(f"\nDigite o nome da série que deseja adicionar no Top {posicao}: ").strip()
        resultado = buscar_filme_serie('serie', nome_serie)

        if resultado:
            titulo = resultado['name']
            descricao = resultado['overview']
            data_lancamento = resultado['first_air_date']

            usuarios[email]['top3_series'][f'Top {posicao}'] = {
                'titulo': titulo,
                'data_lancamento': data_lancamento,
                'descricao': descricao
            }
            print(f"\nSérie '{titulo}' adicionado ao seu Top {posicao} com sucesso!")
        else:
            print(f"\nNão foi possível encontrar informações para a série '{nome_serie}'.")

    print("\nSeu Top 3 séries favoritas foi cadastrada com sucesso!")
    input("\nPressione ENTER para retornar ao menu...")

def exibirtopseries(email):
    if 'top3_series' not in usuarios[email] or not usuarios[email]['top3_series']:
        print("\nVocê ainda não possui série no seu Top 3. Retornando ao menu...")
        time.sleep(3)
        return
    
    clear()
    print("======== [SEU TOP 3 SÉRIES FAVORITAS] ========")
    for posicao in ['Top 1', 'Top 2', 'Top 3']:
        serie = usuarios[email]['top3_series'].get(posicao)
        if serie:
            print(f"\n{posicao.capitalize()}: {serie['titulo']}")
            print(f"\nData de lançamento: {serie['data_lancamento']}")
            print(f"\nDescrição: {serie['descricao']}\n")
            print("==============================================")
    input("\nPressione ENTER para continuar...")
                
def editartopseries(email):
    
    if 'top3_series' not in usuarios[email] or not usuarios[email]['top3_series']:
        print("\nVocê ainda não possui um Top 3 cadastrado. Por favor, crie um Top 3 antes de editar. Retornando ao menu...")
        time.sleep(3)
        return

    clear()
    print("\n======== [TOP 3 SÉRIES ATUAIS] ========")
    for posicao in ['Top 1', 'Top 2', 'Top 3']:
        serie = usuarios[email]['top3_series'].get(posicao)
        if serie:
            print(f"\n{posicao.capitalize()}: {serie['titulo']}")
            print(f"\nData de lançamento: {serie['data_lancamento']}")
            print(f"\nDescrição: {serie['descricao']}\n")
            print("==============================================")

    while True:
            posicao = input("\nDigite a posição (1, 2 ou 3 ou ' ' para cancelar a operação) que deseja editar: ")
            if posicao in ['1', '2', '3']:
                break
            elif posicao == ' ':
                return
            else:
                print("\nOpção inválida! Escolha entre 1, 2 ou 3 ou ' ' para retornar ao.")

    nova_serie = input(f"\nDigite o nome da nova série para o Top {posicao}: ").strip()

    resultado = buscar_filme_serie('serie', nova_serie)

    if resultado:
        usuarios[email]['top3_series'][f'Top {posicao}'] = {
            'titulo': resultado['name'],
            'data_lancamento': resultado['first_air_date'],
            'descricao': resultado['overview']
        }
        print(f"\nTop {posicao} atualizado com sucesso!")
    else:
        print(f"\nNão foi possível adicionar '{nova_serie}' ao Top {posicao}.")

    exibirtopseries(email)      

def excluirtopseries(email):
    if 'top3_series' not in usuarios[email] or not usuarios[email]['top3_series']:
        print("\nVocê não possui um Top 3 cadastrado para excluir. Retornando ao menu...")
        time.sleep(5)
        return

    exibirtopseries(email)

    while True:
        confirmacao = input("\nTem certeza que deseja excluir o seu Top 3 de séries? (s/n): ").strip().lower()
        if confirmacao == 's':
            usuarios[email]['top3_series'] = {}
            print("\nTop 3 de séries excluído com sucesso!")
            input("\nPressione ENTER para retornar ao menu...")
            return
        elif confirmacao == 'n':
            print("\nOperação cancelada. Seu Top 3 de séries permanece intacto.")
            print("\nRetornando ao menu...")
            time.sleep(3)
            return
        else:
            print("\nOpção inválida! Digite novamente")

def menutopseries(email):
    while True:
        clear()
        print("""
======== [SEU TOP 3 SÉRIES FAVORITAS] ========

1. CADASTRAR
2. EDITAR    
3. EXCLUIR
4. EXIBIR  
5. VOLTAR AO MENU PRINCIPAL

==============================================
""")
        
        opcao = int(input("Digite a opção desejada: "))
        
        match opcao:
            case 1:
                addtopseries(email)
            case 2:
                editartopseries(email)
            case 3:
                excluirtopseries(email)
            case 4:
                exibirtopseries(email)
            case 5:
                print("Voltando ao menu principal...")
                break
            case _:
                print("Opção inválida! Digite um número entre 1 e 5.")
                        
def menu_pos_login(email):
    nome = usuarios[email]['nome']
    while True:
        clear()
        print(f"""
=============[Bem-vindo(a), {nome}!]=============
        
            
1. Buscar filmes/séries.
2. Meu top 3 filmes favoritos.
3. Meu top 3 séries favoritas.

0. SAIR

=================================================""")
        opcao = int(input("\nDigite o número da opção desejada: "))
        match opcao:
            case 0:
                return
            case 1:
                while True:
                    clear()
                    print("======== [BUSCAR FILMES/SÉRIES] ========")
                    tipo_busca = input("\nVocê deseja procurar um filme ou uma série? (filme/serie): ")
                    if tipo_busca in ["filme", "serie"]:
                        break
                    print("\nOpção inválida! Digite 'filme' ou 'serie'.")
                
                nome_busca = input(f"\nDigite o nome do(a) {tipo_busca} que deseja pesquisar: ").strip()
                
                resultado = buscar_filme_serie(tipo_busca, nome_busca)
                exibir_informacoes(resultado, tipo_busca)
            case 2:
                menutopfilmes(email)                
            case 3:
                menutopseries(email)
            case _:
                print("\nOpção inválida!.")
                input("\nPressione ENTER para digitar novamente...")
            
def cadastrar_usuario():
    while True:
        clear()
        print("======== [REALIZAR CADASTRO] ========")
        email = input("\nDigite o seu email para cadastro: ").strip()
        
        if email in usuarios:
            print("\nEsse email já está cadastrado. Por favor, use um email diferente.")
            return
        
        nome = input("\nDigite o seu nome: ").strip()
        
        if not nome:
            print("\nO nome não pode estar vazio. Por favor, digite novamente.")
            continue
        
        while True:
            senha = input("\nDigite uma senha (mínimo de 6 caracteres): ").strip()
            
            if len(senha) < 6:
                print("\nA senha deve ter pelo menos 6 caracteres. Por favor, tente novamente.")
            else:
                usuarios[email] = {'nome': nome, 'senha': senha}
                print("\nUsuário cadastrado com sucesso!")
                return

def login():
    clear()
    print("======== [REALIZAR LOGIN] ========")
    email = input("\nDigite o seu email: ")
    senha = input("\nDigite a sua senha: ")
    if email in usuarios and usuarios[email]['senha'] == senha:
        print("\nLogin bem-sucedido!")
        print(
          "====================================")
        menu_pos_login(email)
    else:
        print("\nEmail ou senha incorretos. Tente novamente.")

def menu():
    while True:
        clear()
        print("""
====== BEM-VINDO A NOSSA WIKI DOS FILMES E SERIES ======
        
1. Fazer login
2. Criar conta
3. Sair
        
========================================================
""")
        
        try:
            escolha = int(input("Digite a opção desejada: "))
            
            if escolha == 1:
                login()
            elif escolha == 2:
                cadastrar_usuario()
            elif escolha == 3:
                print("Saindo do programa...")
                break
            else:
                print("Opção inválida! Por favor, digite um número entre 1 e 3.")
        except ValueError:
            print("Entrada inválida! Por favor, digite um número entre 1 e 3.")

menu()