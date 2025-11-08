import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import importlib.util


def _load_tsp_class():
    try:
        from TSP import TSP
        return TSP
    except Exception:
        path = os.path.join(os.path.dirname(__file__), 'TSP.py')
        spec = importlib.util.spec_from_file_location('TSP', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.TSP


TSP = _load_tsp_class()


class TSPInterface:
    """UI enxuta para o Problema do Caixeiro Viajante (TSP) - versão em português de identificadores.

    Observação: os métodos do backend `TSP` também fornecem aliases em português; aqui a interface usa
    esses nomes em português para variáveis e callbacks.
    """

    def __init__(self, root):
        self.root = root
        self.root.title('Problema do Caixeiro Viajante - TSP')
        self.tsp = None
        self.rota_tsp = None
        self._construir_interface()

    def _construir_interface(self):
        main = ttk.Frame(self.root, padding=8)
        main.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Linha 0: tamanho, gerar problema, inicializador
        ttk.Label(main, text='Número de cidades (>=30):').grid(row=0, column=0, sticky=tk.W)
        self.num_cidades_var = tk.StringVar(value='30')
        ttk.Entry(main, textvariable=self.num_cidades_var, width=6).grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Button(main, text='Gerar Problema', command=self.gerar_problema).grid(row=0, column=2, padx=6)

        ttk.Label(main, text='Inicializador:').grid(row=0, column=3, sticky=tk.W, padx=(12, 0))
        self.inicializador_var = tk.StringVar(value='Aleatória')
        opcoes_inicializador = ['Aleatória', 'Vizinho mais próximo']
        self.init_combo = ttk.Combobox(main, textvariable=self.inicializador_var, values=opcoes_inicializador, state='readonly', width=18)
        self.init_combo.grid(row=0, column=4, padx=4)
        ttk.Button(main, text='Gerar Solução Inicial', command=self.gerar_solucao_inicial).grid(row=0, column=5, padx=6)

        # Linha 1: seleção de método e executar
        ttk.Label(main, text='Método de busca local:').grid(row=1, column=0, sticky=tk.W, pady=8)
        self.metodo_var = tk.StringVar(value='Subida de encosta')
        opcoes_metodos = [
            'Subida de encosta',
            'Subida de encosta com tentativas',
            'Têmpera simulada',
            'Algoritmos genéticos',
        ]
        self.method_combo = ttk.Combobox(main, textvariable=self.metodo_var, values=opcoes_metodos, state='readonly', width=36)
        self.method_combo.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Button(main, text='Executar Método', command=self.executar_metodo).grid(row=1, column=5, padx=6)

        # Linha 2+: área de resultados e canvas
        ttk.Label(main, text='Resultados:').grid(row=2, column=0, sticky=tk.W, pady=(8, 0))
        self.texto_resultados = tk.Text(main, width=70, height=12, wrap=tk.WORD)
        self.texto_resultados.grid(row=3, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=4)

        # Canvas matplotlib na coluna 6
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main)
        self.canvas.get_tk_widget().grid(row=0, column=6, rowspan=6, padx=10, pady=4)

        # Configura pesos de grid
        for i in range(6):
            main.columnconfigure(i, weight=0)
        main.columnconfigure(6, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def _adicionar_resultado(self, texto):
        self.texto_resultados.insert(tk.END, texto)
        self.texto_resultados.see(tk.END)

    def gerar_problema(self):
        try:
            n = int(self.num_cidades_var.get())
        except ValueError:
            messagebox.showerror('Erro', 'Informe um número inteiro válido para o tamanho do problema.')
            return
        if n < 30:
            messagebox.showerror('Erro', 'O número de cidades deve ser pelo menos 30.')
            return
        try:
            self.tsp = TSP(n)
            self.rota_tsp = None
            self._adicionar_resultado(f'Problema gerado: {n} cidades\n')
            self.desenhar_grafo()
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao gerar problema TSP: {e}')

    def gerar_solucao_inicial(self):
        if not self.tsp:
            messagebox.showerror('Erro', 'Primeiro gere o problema (Gerar Problema).')
            return
        init_method = self.inicializador_var.get()
        if init_method == 'Vizinho mais próximo':
            try:
                rota = self.tsp.vizinho_mais_proximo(inicio=0)
            except Exception as e:
                messagebox.showerror('Erro', f'Falha no inicializador Vizinho mais próximo: {e}')
                return
        else:
            rota = self.tsp.gerar_solucao_inicial()
        dist = self.tsp.calcular_comprimento_rota(rota)
        self.rota_tsp = rota
        self._adicionar_resultado(f"Rota inicial ({init_method}): {' -> '.join(map(str, rota))}\nDistância: {dist:.2f}\n\n")
        self.desenhar_grafo(rota)

    def executar_metodo(self):
        if not self.tsp:
            messagebox.showerror('Erro', 'Primeiro gere o problema (Gerar Problema).')
            return
        method = self.metodo_var.get()
        if method == 'Subida de encosta':
            rota, dist = self.tsp.subida_de_encosta()
        elif method == 'Subida de encosta com tentativas':
            rota, dist = self.tsp.subida_de_encosta_com_tentativas()
        elif method == 'Têmpera simulada':
            rota, dist = self.tsp.tempera_simulada()
        elif method == 'Algoritmos genéticos':
            rota, dist = self.tsp.algoritmo_genetico()
        else:
            messagebox.showerror('Erro', 'Método desconhecido')
            return
        self.rota_tsp = rota
        self._adicionar_resultado(f"Método: {method}\nDistância total: {dist:.2f}\nRota: {' -> '.join(map(str, rota))}\n\n")
        self.desenhar_grafo(rota)

    def desenhar_grafo(self, rota=None):
        self.ax.clear()
        if not self.tsp:
            self.ax.text(0.5, 0.5, 'Nenhum problema gerado', horizontalalignment='center', verticalalignment='center')
            self.canvas.draw()
            return
        n = self.tsp.num_cidades
        G = nx.complete_graph(n)
        pos = nx.circular_layout(G)
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color='lightblue', node_size=200)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=8)
        # If rota fornecida, destacar arestas da rota
        if rota:
            edges = [(rota[i], rota[(i + 1) % len(rota)]) for i in range(len(rota))]
            nx.draw_networkx_edges(G, pos, ax=self.ax, edgelist=edges, edge_color='red', width=2)
        else:
            nx.draw_networkx_edges(G, pos, ax=self.ax, alpha=0.2)
        self.ax.set_title('Grafo TSP' + (' - Rota' if rota else ''))
        self.ax.axis('off')
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = TSPInterface(root)
    root.mainloop()


if __name__ == '__main__':
    main()