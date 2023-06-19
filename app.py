from flask import Flask, request, jsonify
import random
import string

class Chamada:
    def _init_(self, nome, numero):
        self.nome = nome
        self.numero = numero

class Usuario:
    def _init_(self, username, password):
        self.username = username
        self.password = password
        self.token = None

class GerenciadorChamadas:
    def _init_(self):
        self.chamadas = []
        self.usuarios = []

    def adicionar_chamada(self, chamada):
        self.chamadas.append(chamada)
        print("Chamada adicionada com sucesso!")

    def exibir_chamadas(self):
        if self.chamadas:
            print("Lista de chamadas:")
            for i, chamada in enumerate(self.chamadas):
                print(f"{i+1}. Nome: {chamada.nome}, Número: {chamada.numero}")
        else:
            print("Não há chamadas registradas.")

    def remover_chamada(self, indice):
        if 1 <= indice <= len(self.chamadas):
            chamada_removida = self.chamadas.pop(indice - 1)
            print(f"A chamada de {chamada_removida.nome} foi removida.")
        else:
            print("Índice inválido.")

    def criar_usuario(self, username, password):
        criar_usuario = input("Digite um usuário : ")
        criar_senha = input("Digite uma senha : ")
        novo_usuario = Usuario(username, password)
        self.usuarios.append(novo_usuario)
        print("Usuário criado com sucesso!")

    def fazer_login(self, username, password):
        login_usuario = input("Digite seu usuário novo : ")
        login_senha = input("Digite sua senha : ")
        for usuario in self.usuarios:
            if usuario.username == username and usuario.password == password:
                token = self.gerar_token()
                usuario.token = token
                print(f"Login bem-sucedido! Seu token de autenticação é: {token}")
                return
        print("Usuário ou senha inválidos.")

    def gerar_token(self):
        token = input("Digite seu Token de Autentificação : ")
        caracteres = string.ascii_letters + string.digits
        token = ''.join(random.choice(caracteres) for _ in range(10))
        return token

    def autenticar_token(self, token):
        for usuario in self.usuarios:
            if usuario.token == token:
                return True
        return False

gerenciador = GerenciadorChamadas()
app = Flask ('name')

@app.route('/chamadas', methods=['POST'])
def adicionar_chamada():
    if not gerenciador.autenticar_token(request.headers.get('Authorization')):
        return jsonify({'error': 'Token inválido'}), 401

    data = request.get_json()
    nome = data.get('nome')
    numero = data.get('numero')
    chamada = Chamada(nome, numero)
    gerenciador.adicionar_chamada(chamada)
    return jsonify({'message': 'Chamada adicionada com sucesso!'})

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    gerenciador.criar_usuario(username, password)
    return jsonify({'message': 'Usuário criado com sucesso!'})

@app.route('/login', methods=['POST'])
def fazer_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    gerenciador.fazer_login(username, password)
    return jsonify({'message': 'Login realizado com sucesso!'})

app.run(host='0.0.0.0', port=5000)