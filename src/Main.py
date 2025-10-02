from io_problema import construir_grafo
from PickingSlotting import PickingSlotting

def main():
    nos, grafo = construir_grafo()
    ps = PickingSlotting(nos, grafo)

    caminho, custo = ps.resolver_picking(0, [10,15,9,6],"AMPLITUDE",fechar_ciclo=True)
    print("CAMINHO: ", caminho)
    print("CUSTO: ", custo)

    caminho2, custo2 = ps.resolver_picking(0,[10,15,9,6],"AMPLITUDE",fechar_ciclo=False)
    print("CAMINHO2: ", caminho2)
    print("CUSTO2: ", custo2)

    ranking = ps.rank_slots_por_distancia(0, [2,10,11,13], method="AMPLITUDE")
    print("Ranking: ", ranking)




if __name__ == "__main__":
    main()







