from pathlib import Path
import ast


def caminho_problema(arquivo : str) -> Path:
    raiz = Path(__file__).resolve().parents[1]
    arq = raiz / 'data' /arquivo
    if not arq.exists():
        raise FileNotFoundError(f"Não encontrou o arquivo: {arq}")
    return arq

def ler_problema(arquivo: str ) -> str:
    return caminho_problema(arquivo).read_text(encoding="utf-8")

def parse_linha(linha:str) -> tuple[int, list]:
    linha = linha.strip()
    u_str, rhs = linha.split(':', 1)
    u = int(u_str.strip())
    viz = ast.literal_eval(rhs.strip())
    return u, viz

def construir_grafo(arquivo: str) -> tuple[list[int], list[list[tuple[int, float]]]]:
    texto = ler_problema(arquivo)

    linhas = []
    for ln in texto.splitlines():
        s = ln.strip()
        if s and not s.startswith('#'):
            linhas.append(s)

    adj: dict[int, list] = {}
    for ln in linhas:
        u, viz = parse_linha(ln)
        adj[u] = viz

    total = max(adj.keys()) + 1 if adj else 0
    nos = list(range(total))

    for u in nos:
        adjacentes = adj.get(u, [])
        norm : list[tuple[int, float]] = []
        for item in adjacentes:
            if isinstance(item, int):
                norm.append((item, 1.0))
            else:
                v, w = item
                norm.append((int(v), float(w)))
        adj[u] = sorted(norm, key=lambda t: t[0])

    grafo = [adj[u] for u in nos]
    return nos, grafo

def main():
    nos, grafo = construir_grafo("problema.txt")
    print("nós: ", len(nos))
    print("Adj[0]: ", grafo[0])

if __name__ == "__main__":
        main()






