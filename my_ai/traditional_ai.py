import copy

import board

def stari_posibile(stare_joc_parinte, jucator, depth):
    configuratii_posibile = []
    piese_tabla = stare_joc_parinte.piese_tabla

    if depth == 3:
        stare_joc_parinte = None

    for index, valoare in enumerate(piese_tabla):
        if valoare == 0:
            aux_piese_tabla = copy.deepcopy(piese_tabla)
            aux_piese_tabla[index] = jucator
            configuratii_posibile.append(board.StareJoc(tabla=aux_piese_tabla, GUI=False, parinte=stare_joc_parinte))

    return configuratii_posibile


def min_max_pune_piese(stare_joc: board.StareJoc, jucator, depth=3):
    # configuratie_tabla_rezultata = np.random.choice([-1, 0, 1], size=24)  # date de test random
    # print(stare_joc.piese_tabla)
    # print(jucator)
    # print(stare_joc.check_castigator(jucator))
    # print(stare_joc.check_castigator(-jucator))
    if depth <= 0 or stare_joc.check_castigator(jucator) or stare_joc.check_castigator(-jucator):
        stare_joc.estimare = stare_joc.estimare_scor(depth, -jucator) - stare_joc.estimare_scor(depth, jucator)
        # print(f"depth = {depth} "
        #       f"castigator = {stare_joc.check_castigator(jucator) or stare_joc.check_castigator(-jucator)} "
        #       f"scor = {stare_joc.estimare}")
        return stare_joc

    stari = stari_posibile(stare_joc, jucator, depth)
    # print(f"mutari posibile {len(stari)}\n")

    mutari_cu_estimare = [min_max_pune_piese(stare, -jucator, depth - 1) for stare in stari]
    # for mutare in mutari_posibile:
    #     stare_nou = board.StareJoc()
    #     min_max_pune_piese()

    # print("AI MOVE")
    if jucator == 1:
        # daca jucatorul este JMAX aleg estimarea maxima
        best_move = max(mutari_cu_estimare, key=lambda x: x.estimare)
    else:
        best_move = min(mutari_cu_estimare, key=lambda x: x.estimare)
    return best_move
