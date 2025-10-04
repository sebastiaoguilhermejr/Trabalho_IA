from io_problema import construir_grafo
from PickingSlotting import PickingSlotting


def get_grafo():
    nos, grafo = construir_grafo()
    return nos, grafo

def get_picking_slotting():
    nos, grafo = get_grafo()
    return PickingSlotting(nos, grafo)

def get_caminho_custo(doca, picklist, method="AMPLITUDE", fechar_ciclo=True):
    ps = get_picking_slotting()
    caminho, custo = ps.resolver_picking(doca, picklist, method, fechar_ciclo=fechar_ciclo)
    return caminho, custo

def get_caminho_custo_sem_ciclo(doca, picklist, method="AMPLITUDE"):
    ps = get_picking_slotting()
    caminho, custo = ps.resolver_picking(doca, picklist, method, fechar_ciclo=False)
    return caminho, custo

def get_ranking(doca, slots, method="AMPLITUDE"):
    ps = get_picking_slotting()
    ranking = ps.rank_slots_por_distancia(doca, slots, method=method)
    return ranking

def main():
    caminho, custo = get_caminho_custo(0, [10,15,9,6], "AMPLITUDE", fechar_ciclo=True)
    print("CAMINHO: ", caminho)
    print("CUSTO: ", custo)

    caminho2, custo2 = get_caminho_custo_sem_ciclo(0, [10,15,9,6], "AMPLITUDE")
    print("CAMINHO2: ", caminho2)
    print("CUSTO2: ", custo2)

    ranking = get_ranking(0, [2,10,11,13], method="AMPLITUDE")
    print("Ranking: ", ranking)


if __name__ == "__main__":
    main()







