from pathlib import Path
import ast
from BuscaNP import BuscaNP

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

grafo =  [adj[u] for u in nos]

b = BuscaNP()
inicio, fim = 5, 27
caminhoAmplitude = b.amplitude(inicio,fim,nos,grafo)
print(f"Caminho amplitude: {caminhoAmplitude}, Custo: {len(caminhoAmplitude) -1}")

caminhoProfundidade = b.profundidade(inicio,fim,nos,grafo)
print(f"Caminho profundidade: {caminhoProfundidade}, Custo: {len(caminhoProfundidade) -1}")

caminhoProfundidadeLimitada = b.prof_limitada(inicio,fim,nos,grafo,20)
print(f"Caminho profundidade limitda: {caminhoProfundidadeLimitada}, Custo: {len(caminhoProfundidadeLimitada) -1}")


caminhoAprofundamentoIterativo = b.aprof_iterativo(inicio,fim,nos,grafo,10)
print(f"Caminho aprofundamento iterativo: {caminhoAprofundamentoIterativo}, Custo: {len(caminhoAprofundamentoIterativo) -1}")

caminhoBuscaBidirecional = b.bidirecional(inicio,fim,nos,grafo)
print(print(f"Caminho Busca Bidirecional: {caminhoBuscaBidirecional}, Custo: {len(caminhoBuscaBidirecional) -1}"))




