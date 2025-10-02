from pathlib import Path
import ast


def caminho_problema() -> Path:
    raiz = Path(__file__).resolve().parents[1]
    arq = raiz / 'data' /'problema.txt'
    if not arq.exists():
        raise FileNotFoundError(f"Não encontrou o arquivo: {arq}")
    return arq

def ler_problema() -> str:
    return caminho_problema().read_text(encoding="utf-8")

def parse_linha(linha:str) -> tuple[int, list[int]]:
    linha = linha.strip()
    u_str, rhs = linha.split(':', 1)
    u = int(u_str.strip())
    viz = ast.literal_eval(rhs.strip())
    return u, [int(v) for v in viz]

def construir_grafo() -> tuple[list[int], list[list[int]]]:
    texto = ler_problema()

    linhas = []
    for ln in texto.splitlines():
        s = ln.strip()
        if s and not s.startswith('#'):
            linhas.append(s)

    adj = {}
    for ln in linhas:
        u, viz = parse_linha(ln)
        adj[u] = viz

    total = 30
    nos = list(range(total))

    for u in nos:
        adj.setdefault(u, [])
        adj[u] = sorted(adj[u])

    grafo = [adj[u] for u in nos]
    return nos, grafo






