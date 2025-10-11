from typing import Optional, List, Tuple, Sequence, Union
from math import inf
from BuscaNP import BuscaNP
from BuscaP import busca as BuscaP


class PickingSlotting(object):
    def __init__(self, nos: Sequence[int], grafo: Sequence[Sequence[tuple[int, float]]]):
        self.nos: list[int] = list(nos)
        # Grafo ponderado
        self.grafo_p: list[list[tuple[int, float]]] = [list(adj) for adj in grafo]
        # Grafo não ponderado
        self.grafo_np: list[list[int]] = [[v for (v, _) in adj] for adj in self.grafo_p]
        self.buscaNP = BuscaNP()
        self.buscaP = BuscaP()

    def caminho_e_custo(self, method: str, inicio: int, fim: int, *,
                        lim: Optional[int] = None, lim_max: Optional[int] = None
                        ) -> Optional[Tuple[List[int], float]]:
        # Helpers
        def possui_peso_naoUnitario() -> bool:
            return any(float(w) != 1.0 for adj in self.grafo_p for _, w in adj)

        def numero_passos(caminho: List[int]) -> float:
            return float(max(0, len(caminho) - 1))

        def soma_pesos(caminho: List[int]) -> float:
            total = 0.0
            for u, v in zip(caminho, caminho[1:]):
                w = next((pw for (viz, pw) in self.grafo_p[u] if viz == v), 1.0)
                total += w
            return total

        def normalizar_saida(saida: Optional[Union[List[int], Tuple[List[int], float]]]
                             ) -> Optional[Tuple[List[int], float]]:
            if saida is None:
                return None
            if isinstance(saida, tuple):
                caminho, custo = saida
                return caminho, float(custo)
            caminho = saida
            return caminho, float(soma_pesos(caminho))

        method = method.upper().strip()

        # ---------- NÃO PONDERADOS ----------
        if method in {"AMPLITUDE", "PROFUNDIDADE", "PROFUNDIDADE_LIMITADA", "PROF_LIMITADA",
                      "APROFUNDAMENTO_ITERATIVO", "BUSCA BIDIRECIONAL", "BIDIRECIONAL"}:
            if possui_peso_naoUnitario():
                raise ValueError("Grafo com pesos ≠ 1: use CUSTO_UNIFORME, GREEDY, A_ESTRELA ou AIA_ESTRELA.")

            if method == "AMPLITUDE":
                cam = self.buscaNP.amplitude(inicio, fim, self.nos, self.grafo_np)
            elif method == "PROFUNDIDADE":
                cam = self.buscaNP.profundidade(inicio, fim, self.nos, self.grafo_np)
            elif method in {"PROFUNDIDADE_LIMITADA", "PROF_LIMITADA"}:
                if lim is None:
                    raise ValueError("Profundidade limitada requer lim")
                cam = self.buscaNP.prof_limitada(inicio, fim, self.nos, self.grafo_np, lim)
            elif method == "APROFUNDAMENTO_ITERATIVO":
                if lim_max is None:
                    raise ValueError("Aprofundamento iterativo requer lim_max")
                cam = self.buscaNP.aprof_iterativo(inicio, fim, self.nos, self.grafo_np, lim_max)
            else:  # BIDIRECIONAL
                cam = self.buscaNP.bidirecional(inicio, fim, self.nos, self.grafo_np)

            return None if not cam else (cam, numero_passos(cam))

        # ---------- PONDERADOS ----------
        elif method in {"CUSTO_UNIFORME", "GREEDY", "A_ESTRELA", "AIA_ESTRELA"}:
            res = None
            if method == "CUSTO_UNIFORME":
                res = self.buscaP.custo_uniforme(inicio, fim, self.nos, self.grafo_p)
            elif method == "GREEDY":
                res = self.buscaP.greedy(inicio, fim, self.nos, self.grafo_p)
            elif method == "A_ESTRELA":
                res = self.buscaP.a_estrela(inicio, fim, self.nos, self.grafo_p)
            elif method == "AIA_ESTRELA":
                res = self.buscaP.aia_estrela(inicio, fim, self.nos, self.grafo_p)
                if res is None:
                    return None
                cam, custo, _ = res
                return cam, float(custo)
            return normalizar_saida(res)

        else:
            raise ValueError(f"Método desconhecido: {method}")

    def fechamento_metrico(self, P: list[int], *, method: str, lim: Optional[int] = None,
                           lim_max: Optional[int] = None):
        n = len(P)
        M = [[float('inf')] * n for _ in range(n)]

        for i in range(n):
            M[i][i] = 0

        for i, s in enumerate(P):
            for j, t in enumerate(P):
                if i == j:
                    continue
                res = self.caminho_e_custo(method, s, t, lim=lim, lim_max=lim_max)
                if res is not None:
                    _, custo = res
                    M[i][j] = float(custo)
        return M

    def rota_vizinho_mais_proximo(self, M, start_idx=0):
        n = len(M)
        if n == 0:
            return []
        nao_visitados = set(range(n))
        nao_visitados.discard(start_idx)
        ordem_idx = [start_idx]
        atual = start_idx
        while nao_visitados:
            prox = min(nao_visitados, key=lambda j: (M[atual][j], j))
            ordem_idx.append(prox)
            nao_visitados.remove(prox)
            atual = prox
        return ordem_idx

    def traduzir_rota_vizinho_mais_proximo(self, M, P, start_idx=0):
        assert len(M) == len(P)
        ordem_idx = self.rota_vizinho_mais_proximo(M, start_idx)
        return [P[i] for i in ordem_idx]

    def custo_e_rota_expandida(self, ordem_idx: list[int], P: list[int], method: str = "AMPLITUDE",
                               lim: Optional[int] = None, lim_max: Optional[int] = None,
                               fechar_ciclo: bool = False) -> tuple[list[int], float]:
        if not ordem_idx:
            return [], 0.0

        pares = list(zip(ordem_idx, ordem_idx[1:]))
        if fechar_ciclo and len(ordem_idx) > 1:
            pares.append((ordem_idx[-1], ordem_idx[0]))

        caminho_total: list[int] = []
        custo_total: float = 0.0

        for i_idx, j_idx in pares:
            s, t = P[i_idx], P[j_idx]
            res = self.caminho_e_custo(method, s, t, lim=lim, lim_max=lim_max)
            if res is None:
                return [], inf
            cam, custo = res
            if not caminho_total:
                caminho_total.extend(cam)
            else:
                caminho_total.extend(cam[1:])
            custo_total += float(custo)

        return caminho_total, custo_total

    def resolver_picking(self, doca: int, picklist: list[int], method: str, *, lim: Optional[int] = None,
                         lim_max: Optional[int] = None,
                         fechar_ciclo: bool = False) -> tuple[list[int], float]:
        P = [doca] + list(picklist)
        matriz = self.fechamento_metrico(P, method=method, lim=lim, lim_max=lim_max)

        ordem_idx = self.rota_vizinho_mais_proximo(matriz, start_idx=0)

        caminho_total, custo_total = self.custo_e_rota_expandida(
            ordem_idx, P, method=method, lim=lim, lim_max=lim_max, fechar_ciclo=fechar_ciclo
        )
        return caminho_total, custo_total

    def rank_slots_por_distancia(self, doca: int, slots: Optional[list[int]] = None, method: str = "AMPLITUDE", *,
                                 lim: Optional[int] = None, lim_max: Optional[int] = None) -> list[tuple[int, float]]:
        if slots is None:
            slots = [n for n in self.nos if n != doca]
        else:
            slots = sorted({s for s in slots if s != doca})

        ranking = []
        for s in slots:
            res = self.caminho_e_custo(method, doca, s, lim=lim, lim_max=lim_max)
            if res is None:
                dist = float("inf")
            else:
                _, custo = res
                dist = float(custo)
            ranking.append((s, dist))

        ranking.sort(key=lambda x: (x[1], x[0]))
        return ranking
