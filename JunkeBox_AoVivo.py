# Projeto Freelancer e de Estudos em Python
# Backend simples usando Flask e Socket.IO para comunicação em tempo real.

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '!TheLoreansBand!'  # Troque por uma chave segura
socketio = SocketIO(app)

# Lista de músicas disponíveis
musicas_disponiveis = [
    {"id": 1, "titulo": "Waitin For The End - Linkin Park"},
    {"id": 2, "titulo": "Wasting Love - Iron Maiden"},
    {"id": 3, "titulo": "Eu Quero Ver o Oco - Raimundos"},
    {"id": 4, "titulo": "Roda Roda Vira - Mamonas assassinas"},
]

# Lista de músicas escolhidas
fila_escolhas = []

# Rota principal para o dispositivo público
@app.route('/')
def index():
    return render_template('index.html', musicas=musicas_disponiveis)

# Endpoint para receber a escolha de música
def adicionar_a_fila(musica):
    fila_escolhas.append(musica)
    socketio.emit('atualizar_fila', fila_escolhas)

@app.route('/escolher', methods=['POST'])
def escolher():
    dados = request.json
    musica_id = dados.get('musica_id')

    # Valida a música escolhida
    musica = next((m for m in musicas_disponiveis if m["id"] == musica_id), None)
    if not musica:
        return jsonify({"erro": "Música não encontrada"}), 404

    adicionar_a_fila(musica)
    return jsonify({"mensagem": "Música adicionada à fila!"})

# Rota para o painel no palco
@app.route('/painel')
def painel():
    return render_template('painel.html')

# Rota para adicionar músicas (admin)
@app.route('/admin/adicionar', methods=['POST'])
def adicionar_musica():
    dados = request.json
    titulo = dados.get('titulo')

    if not titulo:
        return jsonify({"erro": "Título da música é obrigatório"}), 400

    nova_musica = {"id": len(musicas_disponiveis) + 1, "titulo": titulo}
    musicas_disponiveis.append(nova_musica)
    socketio.emit('atualizar_musicas', musicas_disponiveis)
    return jsonify({"mensagem": "Música adicionada com sucesso!", "musica": nova_musica})

# Rota para remover músicas (admin)
@app.route('/admin/remover', methods=['POST'])
def remover_musica():
    dados = request.json
    musica_id = dados.get('musica_id')

    global musicas_disponiveis
    musicas_disponiveis = [m for m in musicas_disponiveis if m["id"] != musica_id]
    socketio.emit('atualizar_musicas', musicas_disponiveis)
    return jsonify({"mensagem": "Música removida com sucesso!"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
