from functools import lru_cache
from typing import Optional, List, Tuple
from io_problema import construir_grafo
from PickingSlotting import PickingSlotting


@lru_cache(maxsize=1)
def get_grafo() -> Tuple[List[int], List[List[Tuple[int, float]]]]:
    nos, grafo = construir_grafo("problema_ponderado.txt")
    return nos, grafo

@lru_cache(maxsize=1)
def get_picking_slotting() -> PickingSlotting:
    nos, grafo = get_grafo()
    return PickingSlotting(nos, grafo)


def get_caminho_custo(
    doca: int,
    picklist: List[int],
    method: str = "AMPLITUDE",
    *,
    fechar_ciclo: bool = True,
    lim: Optional[int] = None,
    lim_max: Optional[int] = None,
) -> Tuple[Optional[List[int]], float]:
    ps = get_picking_slotting()
    try:
        caminho, custo = ps.resolver_picking(
            doca, picklist, method, lim=lim, lim_max=lim_max, fechar_ciclo=fechar_ciclo
        )
        return caminho, float(custo)
    except ValueError as e:
        print(f"[ERRO] {e}")

        return None, float("inf")


def get_caminho_custo_sem_ciclo(
    doca: int,
    picklist: List[int],
    method: str = "AMPLITUDE",
    *,
    lim: Optional[int] = None,
    lim_max: Optional[int] = None,
) -> Tuple[Optional[List[int]], float]:
    return get_caminho_custo(
        doca, picklist, method, fechar_ciclo=False, lim=lim, lim_max=lim_max
    )


def get_ranking(
    doca: int,
    slots: List[int],
    method: str = "AMPLITUDE",
    *,
    lim: Optional[int] = None,
    lim_max: Optional[int] = None,
) -> List[Tuple[int, float]]:
    ps = get_picking_slotting()
    try:
        ranking = ps.rank_slots_por_distancia(
            doca, slots, method=method, lim=lim, lim_max=lim_max
        )
        return ranking
    except ValueError:
        return []


def main():
    """
    caminho, custo = get_caminho_custo(0, [10, 15, 9, 6], "AMPLITUDE", fechar_ciclo=True)
    print("CAMINHO:", caminho)
    print("CUSTO:", custo)

    caminho2, custo2 = get_caminho_custo_sem_ciclo(0, [10, 15, 9, 6], "AMPLITUDE")
    print("CAMINHO2:", caminho2)
    print("CUSTO2:", custo2)

    """

    get_grafo.cache_clear()
    get_picking_slotting.cache_clear()

    caminho3, custo3 = get_caminho_custo(0, [10, 15, 2], method="AIA_ESTRELA", fechar_ciclo=True)
    print("CAMINHO3:", caminho3)
    print("CUSTO3:", custo3)





if __name__ == "__main__":
    main()
