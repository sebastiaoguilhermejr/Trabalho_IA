import itertools

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

def carregar_grafo_do_arquivo():
    nos = []
    grafo = []
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data', 'problema.txt')
    try:
        with open(caminho, 'r') as f:
            for linha in f:
                parte_no, parte_adj = linha.split(':')
                no = int(parte_no.strip())
                adj = parte_adj.strip().replace('[', '').replace(']', '').split(',')
                adj = [int(x) for x in adj if x.strip()]
                nos.append(no)
                grafo.append(adj)
    except Exception as e:
        return [], [], [], '', f"Erro ao ler problema.txt: {e}"
    nos_str = ','.join(str(n) for n in nos)
    grafo_str = '\n'.join(','.join(str(x) for x in adj) for adj in grafo)
    return nos, grafo, nos_str, grafo_str, None

def exibir_grafo():
    global tipo_var, inicio_var, destino_var, pontos_var, opcoes_label
    metodo = tipo_var.get()
    inicio_str = inicio_var.get()
    destino_str = destino_var.get()
    pontos_str = pontos_var.get()
    lim_str = lim_var.get()
    lim_max_str = lim_max_var.get()
    try:
        inicio = int(inicio_str)
        destino = int(destino_str)
        pontos = [int(x) for x in pontos_str.split(',') if x.strip()] if pontos_str else []
        lim = int(lim_str) if lim_str else None
        lim_max = int(lim_max_str) if lim_max_str else None
    except ValueError:
        messagebox.showerror('Erro', 'Informe valores inteiros para início, destino, pontos intermediários, lim e lim_max.')
        return
    nos, grafo, nos_str, grafo_str, erro = carregar_grafo_do_arquivo()
    if erro:
        messagebox.showerror('Erro', erro)
        return
    # Gerar subgrafo do caminho percorrido
    try:
        from PickingSlotting import PickingSlotting
        ps = PickingSlotting(nos, grafo)
        picklist = pontos + [destino]
        if metodo in ['PROFUNDIDADE_LIMITADA', 'PROF_LIMITADA', 'APROFUNDAMENTO_ITERATIVO']:
            caminho, custo = ps.resolver_picking(inicio, picklist, metodo, lim=lim, lim_max=lim_max)
        else:
            caminho, custo = ps.resolver_picking(inicio, picklist, metodo)
        # Mostrar opções e melhor caminho
        opcoes = []
        melhor_caminho = caminho
        melhor_custo = custo
        # Para métodos que retornam apenas o melhor, exibe só ele
        opcoes.append((caminho, custo))
        # Exibir na interface
        texto_opcoes = ''
        for idx, (cam, cst) in enumerate(opcoes):
            texto_opcoes += f'Opção {idx+1}: {cam} | Custo: {cst}\n'
        texto_opcoes += f'\nMelhor caminho: {melhor_caminho} | Menor custo: {melhor_custo}'
        opcoes_label.config(text=texto_opcoes)
    except Exception as e:
        caminho = None
        opcoes_label.config(text='Não foi possível encontrar caminho.')

        if caminho and len(caminho) > 1:
            G = nx.Graph()
            edges_caminho = list(zip(caminho, caminho[1:]))
            G.add_nodes_from(caminho)
            G.add_edges_from(edges_caminho)
            pos = {}
            # Distribuir os nós em linha
            for idx, node in enumerate(caminho):
                pos[node] = (idx, 0)
            plt.figure(figsize=(1.5 * len(caminho), 2))
            nx.draw(G, pos, with_labels=True, node_color='orange', edge_color='red', width=2, font_weight='bold', node_size=600)
            plt.title(f'Caminho: {caminho}')
        else:
            # Se não há caminho, mostrar grafo completo
            G = nx.Graph()
            for i, adj in zip(nos, grafo):
                for j in adj:
                    G.add_edge(i, j)
            pos = nx.circular_layout(G)
            plt.figure(figsize=(5, 4))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
            plt.title('Grafo completo (sem caminho)')

        img_path = os.path.join(os.path.dirname(__file__), 'grafo_temp.png')
        plt.savefig(img_path)
        plt.close()
        # Exibir imagem no Tkinter
        try:
            img = Image.open(img_path)
            img = img.resize((300, 240))
            img_tk = ImageTk.PhotoImage(img)
            if hasattr(exibir_grafo, 'img_label'):
                exibir_grafo.img_label.config(image=img_tk)
                exibir_grafo.img_label.image = img_tk
            else:
                exibir_grafo.img_label = tk.Label(exibir_grafo.root, image=img_tk)
                exibir_grafo.img_label.image = img_tk
                exibir_grafo.img_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao exibir imagem: {e}')
    nos_str = ','.join(str(n) for n in nos)
    grafo_str = '\n'.join(','.join(str(x) for x in adj) for adj in grafo)
    return nos, grafo, nos_str, grafo_str, None

def processar_formulario():
    nos, grafo, nos_str, grafo_str, erro = carregar_grafo_do_arquivo()
    if erro:
        messagebox.showerror('Erro', erro)
    else:
        msg = f'Nós: {nos_str}\nGrafo:\n{grafo_str}'
        messagebox.showinfo('Dados do Grafo', msg)







def main():
    # global já declarado no início da função main
    def mostrar_melhor_caminho():
        metodo = tipo_var.get()
        inicio_str = inicio_var.get()
        destino_str = destino_var.get()
        pontos_str = pontos_var.get()
        lim_str = lim_var.get()
        lim_max_str = lim_max_var.get()
        try:
            inicio = int(inicio_str)
            destino = int(destino_str)
            pontos = [int(x) for x in pontos_str.split(',') if x.strip()] if pontos_str else []
            lim = int(lim_str) if lim_str else None
            lim_max = int(lim_max_str) if lim_max_str else None
        except ValueError:
            messagebox.showerror('Erro', 'Informe valores inteiros para início, destino, pontos intermediários, lim e lim_max.')
            return
        nos, grafo, nos_str, grafo_str, erro = carregar_grafo_do_arquivo()
        if erro:
            messagebox.showerror('Erro', erro)
            return
        # Calcula o menor caminho global usando AMPLITUDE
        from PickingSlotting import PickingSlotting
        ps_global = PickingSlotting(nos, grafo)
        if pontos:
            melhores_global = []
            pontos_sem_destino = [p for p in pontos if p != destino]
            for perm in itertools.permutations(pontos_sem_destino):
                P = [inicio] + list(perm) + [destino]
                matriz = ps_global.fechamento_metrico(P, method='AMPLITUDE')
                ordem_idx = list(range(len(P)))
                caminho_total, custo_total = ps_global.custo_e_rota_expandida(ordem_idx, P, method='AMPLITUDE', fechar_ciclo=False)
                if caminho_total:
                    melhores_global.append((caminho_total, custo_total))
            melhores_global_validos = [(cam, cst) for cam, cst in melhores_global if cam and cst is not None and cst < float('inf')]
            if melhores_global_validos:
                melhores_global_validos.sort(key=lambda x: x[1])
                menor_caminho_global, menor_custo_global = melhores_global_validos[0]
            else:
                menor_caminho_global, menor_custo_global = None, None
        else:
            menor_caminho_global, menor_custo_global = ps_global.caminho_e_custo('AMPLITUDE', inicio, destino)
    # global já declarado no início da função main
        metodo = tipo_var.get()
        inicio_str = inicio_var.get()
        destino_str = destino_var.get()
        pontos_str = pontos_var.get()
        lim_str = lim_var.get()
        lim_max_str = lim_max_var.get()
        try:
            inicio = int(inicio_str)
            destino = int(destino_str)
            pontos = [int(x) for x in pontos_str.split(',') if x.strip()] if pontos_str else []
            lim = int(lim_str) if lim_str else None
            lim_max = int(lim_max_str) if lim_max_str else None
        except ValueError:
            messagebox.showerror('Erro', 'Informe valores inteiros para início, destino, pontos intermediários, lim e lim_max.')
            return
        nos, grafo, nos_str, grafo_str, erro = carregar_grafo_do_arquivo()
        if erro:
            messagebox.showerror('Erro', erro)
            return
        from PickingSlotting import PickingSlotting
        ps = PickingSlotting(nos, grafo)
        melhores = []
        pontos_sem_destino = [p for p in pontos if p != destino]
        print(f'INICIO: {inicio}, DESTINO: {destino}, PONTOS: {pontos}, METODO: {metodo}, LIM: {lim}, LIM_MAX: {lim_max}')
        # Se não há pontos intermediários, só testa o caminho direto
        if not pontos_sem_destino:
            P = [inicio, destino]
            print(f'Testando ordem: {P}')
            matriz = ps.fechamento_metrico(P, method=metodo, lim=lim, lim_max=lim_max)
            print(f'Matriz de custos: {matriz}')
            ordem_idx = [0, 1]
            caminho_total, custo_total = ps.custo_e_rota_expandida(ordem_idx, P, method=metodo, lim=lim, lim_max=lim_max, fechar_ciclo=False)
            print(f'Resultado: Caminho: {caminho_total} | Custo: {custo_total}')
            if caminho_total:
                melhores.append((caminho_total, custo_total))
        else:
            for perm in itertools.permutations(pontos_sem_destino):
                P = [inicio] + list(perm) + [destino]
                print(f'Testando ordem: {P}')
                matriz = ps.fechamento_metrico(P, method=metodo, lim=lim, lim_max=lim_max)
                print(f'Matriz de custos: {matriz}')
                ordem_idx = list(range(len(P)))
                caminho_total, custo_total = ps.custo_e_rota_expandida(ordem_idx, P, method=metodo, lim=lim, lim_max=lim_max, fechar_ciclo=False)
                print(f'Resultado: Caminho: {caminho_total} | Custo: {custo_total}')
                if caminho_total:
                    melhores.append((caminho_total, custo_total))
        if not melhores:
            opcoes_label.config(text='Nenhum caminho encontrado.')
            return
        # Exibe todos os caminhos e custos calculados no console
        print('Caminhos e custos calculados:')
        for idx, (cam, cst) in enumerate(melhores):
            print(f'Opção {idx+1}: {cam} | Custo: {cst}')
        melhores.sort(key=lambda x: x[1])
        melhor_caminho, melhor_custo = melhores[0]
        # Filtra apenas caminhos válidos (custo < infinito e caminho não vazio)
        melhores_validos = [(cam, cst) for cam, cst in melhores if cam and cst is not None and cst < float('inf')]
        if not melhores_validos:
            opcoes_label.config(text='Nenhum caminho válido encontrado.')
            messagebox.showinfo('Melhor Caminho', f'Método: {metodo}\nNenhum caminho válido encontrado.')
            return
        print('Caminhos e custos válidos:')
        for idx, (cam, cst) in enumerate(melhores_validos):
            print(f'Opção {idx+1}: {cam} | Custo: {cst}')
        melhores_validos.sort(key=lambda x: x[1])
        melhor_caminho, melhor_custo = melhores_validos[0]
        texto_opcoes = 'Melhor caminho encontrado pelo método selecionado:\n'
        texto_opcoes += f'{melhor_caminho} | Custo: {melhor_custo}\n\n'
        texto_opcoes += 'Outras opções pelo método selecionado:\n'
        for idx, (cam, cst) in enumerate(melhores_validos[1:]):
            texto_opcoes += f'Opção {idx+2}: {cam} | Custo: {cst}\n'
        if menor_caminho_global and menor_custo_global is not None:
            texto_opcoes += f'\nRecomendação: Menor caminho global (AMPLITUDE):\n{menor_caminho_global} | Custo: {menor_custo_global}\n'
        else:
            texto_opcoes += '\nRecomendação: Não foi possível encontrar o menor caminho global.\n'
        opcoes_label.config(text=texto_opcoes)
        # Mensagem popup informando o melhor caminho escolhido e recomendação
        msg_popup = f'Método: {metodo}\nO melhor caminho escolhido foi: {melhor_caminho}\nCusto: {melhor_custo}'
        if menor_caminho_global and menor_custo_global is not None:
            msg_popup += f'\n\nRecomendação: Menor caminho global (AMPLITUDE):\n{menor_caminho_global} | Custo: {menor_custo_global}'
        else:
            msg_popup += '\n\nRecomendação: Não foi possível encontrar o menor caminho global.'
        messagebox.showinfo('Melhor Caminho', msg_popup)
        # Exibir o caminho percorrido sobre o grafo completo
        if melhor_caminho and len(melhor_caminho) > 1:
            # Grafo completo
            G = nx.Graph()
            for i, adj in zip(nos, grafo):
                for j in adj:
                    G.add_edge(i, j)
            # Destaca os nós e arestas do caminho
            edges_caminho = list(zip(melhor_caminho, melhor_caminho[1:]))
            node_colors = ['orange' if n in melhor_caminho else 'lightblue' for n in G.nodes()]
            edge_colors = ['red' if (u, v) in edges_caminho or (v, u) in edges_caminho else 'gray' for u, v in G.edges()]
            pos = nx.spring_layout(G)
            plt.figure(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, width=2, font_weight='bold', node_size=600)
            plt.title(f'Melhor Caminho Percorrido: {melhor_caminho}')
            img_path = os.path.join(os.path.dirname(__file__), 'grafo_temp.png')
            plt.savefig(img_path)
            plt.close()
            try:
                img = Image.open(img_path)
                img = img.resize((300, 240))
                img_tk = ImageTk.PhotoImage(img)
                if hasattr(exibir_grafo, 'img_label'):
                    exibir_grafo.img_label.config(image=img_tk)
                    exibir_grafo.img_label.image = img_tk
                else:
                    exibir_grafo.img_label = tk.Label(root, image=img_tk)
                    exibir_grafo.img_label.image = img_tk
                    exibir_grafo.img_label.pack(pady=10)
            except Exception as e:
                messagebox.showerror('Erro', f'Falha ao exibir imagem: {e}')
    global tipo_var, inicio_var, destino_var, pontos_var, opcoes_label, lim_var, lim_max_var
    root = tk.Tk()
    root.title('Interface Tkinter')

    label = tk.Label(root, text='Bem-vindo à interface Tkinter!')
    label.pack(pady=10)

    # Campos de entrada para início, pontos intermediários e destino
    inicio_var = tk.StringVar()
    destino_var = tk.StringVar()
    pontos_var = tk.StringVar()
    frame_inputs = tk.Frame(root)
    tk.Label(frame_inputs, text='Início:').pack(side=tk.LEFT)
    tk.Entry(frame_inputs, textvariable=inicio_var, width=5).pack(side=tk.LEFT, padx=5)
    tk.Label(frame_inputs, text='Pontos (separados por vírgula):').pack(side=tk.LEFT)
    tk.Entry(frame_inputs, textvariable=pontos_var, width=15).pack(side=tk.LEFT, padx=5)
    tk.Label(frame_inputs, text='Destino:').pack(side=tk.LEFT)
    tk.Entry(frame_inputs, textvariable=destino_var, width=5).pack(side=tk.LEFT, padx=5)
    # Campos para lim e lim_max
    lim_var = tk.StringVar()
    lim_max_var = tk.StringVar()
    tk.Label(frame_inputs, text='Lim:').pack(side=tk.LEFT)
    tk.Entry(frame_inputs, textvariable=lim_var, width=5).pack(side=tk.LEFT, padx=5)
    tk.Label(frame_inputs, text='Lim_max:').pack(side=tk.LEFT)
    tk.Entry(frame_inputs, textvariable=lim_max_var, width=5).pack(side=tk.LEFT, padx=5)
    frame_inputs.pack(pady=10)

    btn = tk.Button(root, text='Processar', command=processar_formulario)
    btn.pack(pady=10)

    # Combobox para método de busca
    tipo_var = tk.StringVar(value='AMPLITUDE')
    tipo_combo = ttk.Combobox(root, textvariable=tipo_var, state='readonly')
    tipo_combo['values'] = [
        'AMPLITUDE',
        'PROFUNDIDADE',
        'PROFUNDIDADE_LIMITADA',
        'PROF_LIMITADA',
        'APROFUNDAMENTO_ITERATIVO',
        'BUSCA BIDIRECIONAL',
        'BIDIRECIONAL'
    ]
    tipo_combo.pack(pady=10)


    btn_grafo = tk.Button(root, text='Exibir Grafo', command=exibir_grafo)
    btn_grafo.pack(pady=10)

    btn_melhor = tk.Button(root, text='Melhor Caminho', command=mostrar_melhor_caminho)
    btn_melhor.pack(pady=10)

    # Label para mostrar opções de caminhos e melhor caminho
    opcoes_label = tk.Label(root, text='', justify=tk.LEFT, font=('Arial', 10))
    opcoes_label.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()

def processar_formulario():
    nos, grafo, nos_str, grafo_str, erro = carregar_grafo_do_arquivo()
    if erro:
        messagebox.showerror('Erro', erro)
    else:
        msg = f'Nós: {nos_str}\nGrafo:\n{grafo_str}'
        messagebox.showinfo('Dados do Grafo', msg)
    # Removido código Flask. Função agora apenas mostra os dados do grafo em popup.


