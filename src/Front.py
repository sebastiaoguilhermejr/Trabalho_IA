from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx
import Main
from flask import Flask, render_template, request
import os


app = Flask(__name__)

# Certifique-se de que o diretório 'static' exista
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    # Rota principal que renderiza a página HTML. 
    combo_options = ["Amplitude","Profundidade","Profundidade Limitada","Aprofundamento Iterativo","Busca Bidirecional" ]
    return render_template('Site.html')

if__name__=="__main__":
app.run(debug=True)

@app.route('/gerar_grafo', methods=['POST'])
def gerar_grafo():
    #Rota que gera o grafo com base na seleção do usuário.
    graph_type = request.form.get('graph_type')
    file_name = f"grafo_{graph_type}.png"
    file_path = os.path.join('static', file_name)

    # Gere o grafo conforme o tipo
    if graph_type == "Amplitude":
        caminho = Main.caminhoAmplitude
    elif graph_type == "Profundidade":
        caminho = Main.caminhoProfundidade
    elif graph_type == "Profundidade Limitada":
        caminho = Main.caminhoProfundidadeLimitada
    elif graph_type == "Aprofundamento Iterativo":
        caminho = Main.caminhoAprofundamentoIterativo
    elif graph_type == "Busca Bidirecional":
        caminho = Main.caminhoBuscaBidirecional
    else:
        return "Tipo de grafo desconhecido", 400

    G = nx.Graph()
    G.add_nodes_from(caminho)
    edges = [(caminho[i], caminho[i + 1]) for i in range(len(caminho) - 1)]
    G.add_edges_from(edges)
    plt.figure()
    nx.draw(G, with_labels=True, node_size=700, font_size=10, font_weight="bold", edge_color="black", node_color="lightblue")
    plt.title(f"Grafo {graph_type}")
    plt.gcf().canvas.manager.set_window_title(f"Grafo {graph_type}") 
    plt.savefig(file_path)
    plt.close()

    return render_template('Site.html', graph_image=file_name)


if __name__ == '__main__':
    app.run(debug=True)

