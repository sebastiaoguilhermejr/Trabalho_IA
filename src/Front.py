from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx
from BuscaNP import BuscaNP as bnp
import Main

caminhoAmplitude = Main.caminhoAmplitude
caminhoPrfofundidade = Main.caminhoProfundidade
caminhoProfundidadeLimitada = Main.caminhoProfundidadeLimitada
caminhoAprofundamentoIterativo = Main.caminhoAprofundamentoIterativo
caminhoBuscaBidirecional = Main.caminhoBuscaBidirecional


#desenhar grafo em Amplitude
G = nx.Graph()
G.add_nodes_from(caminhoAmplitude)
edges = [(caminhoAmplitude[i], caminhoAmplitude[i + 1]) for i in range(len(caminhoAmplitude) - 1)]
G.add_edges_from(edges)
nx.draw(G, with_labels=True,node_size=700, font_size=10, font_weight="bold", edge_color="black", node_color="lightblue")
plt.title("Grafo Amplitude")
plt.gcf().canvas.manager.set_window_title("Grafo Amplitude") 
plt.show()

#desenhar grafo em Profundidade
G = nx.Graph()
G.add_nodes_from(caminhoPrfofundidade)
edges = [(caminhoPrfofundidade[i], caminhoPrfofundidade[i + 1]) for i in range(len(caminhoPrfofundidade) - 1)]
G.add_edges_from(edges)
nx.draw(G, with_labels=True,node_size=700, font_size=10, font_weight="bold", edge_color="black", node_color="lightblue")
plt.title("Grafo Profundidade")
plt.gcf().canvas.manager.set_window_title("Grafo Profundidade")
plt.show()

#desenhar grafo em Profundidade Limitada
G = nx.Graph()
G.add_nodes_from(caminhoProfundidadeLimitada)
edges = [(caminhoProfundidadeLimitada[i], caminhoProfundidadeLimitada[i + 1]) for i in range(len(caminhoProfundidadeLimitada) - 1)]
G.add_edges_from(edges)
nx.draw(G, with_labels=True,node_size=700, font_size=10, font_weight="bold", edge_color="black", node_color="lightblue")
plt.title("Grafo Profundidade Limitada")
plt.gcf().canvas.manager.set_window_title("Grafo Profundidade Limitada")
plt.show()

#desenhar grafo em Aprofundamento Iterativo
G = nx.Graph()
G.add_nodes_from(caminhoAprofundamentoIterativo)
edges = [(caminhoAprofundamentoIterativo[i], caminhoAprofundamentoIterativo[i + 1]) for i in range(len(caminhoAprofundamentoIterativo) - 1)]
G.add_edges_from(edges)
nx.draw(G, with_labels=True,node_size=700, font_size=10, font_weight="bold", edge_color="black", node_color="lightblue")
plt.title("Grafo Profundidade Iterativa")
plt.gcf().canvas.manager.set_window_title("Grafo Profundidade Iterativa")
plt.show()

#desenhar grafo em Busca Bidirecional
G = nx.Graph()
G.add_nodes_from(caminhoBuscaBidirecional) 
edges = [(caminhoBuscaBidirecional[i], caminhoBuscaBidirecional[i + 1]) for i in range(len(caminhoBuscaBidirecional) - 1)]
G.add_edges_from(edges)
nx.draw(G, with_labels=True,node_size=700, font_size=10, font_weight="bold", edge_color="black", node_color="lightblue")
plt.title("Grafo Busca Bidirecional")
plt.gcf().canvas.manager.set_window_title("Grafo Busca Bidirecional")
plt.show()