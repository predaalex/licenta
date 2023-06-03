import copy
import random
import numpy as np

from board import StareJoc


def min_max_muta_piese(stare_joc: StareJoc, heuristic, jucator_initial, jucator, max_depth=3, depth=3):
    if depth <= 0:
        stare_joc.estimare = stare_joc.estimare_scor(depth, jucator_initial, heuristic)
        return stare_joc

    stari = stari_posibile_muta_piese(stare_joc, jucator, max_depth, depth)

    mutari_cu_estimare = [min_max_muta_piese(stare, heuristic, jucator_initial, -jucator, max_depth, depth - 1) for stare in stari]

    if len(mutari_cu_estimare) == 0:
        # print("end game") # DEBUG
        stare_joc.estimare = -999
        return stare_joc
    # print("AI MOVE")
    if jucator == jucator_initial:
        # daca jucatorul este JMAX aleg estimarea maxima
        best_estimare = max(mutari_cu_estimare, key=lambda x: x.estimare).estimare
        best_mutari = [mutare for mutare in mutari_cu_estimare if mutare.estimare == best_estimare]
        best_move = random.choice(best_mutari)
    else:
        best_estimare = min(mutari_cu_estimare, key=lambda x: x.estimare).estimare
        best_mutari = [mutare for mutare in mutari_cu_estimare if mutare.estimare == best_estimare]
        best_move = random.choice(best_mutari)
    return best_move


def min_max_pune_piese(stare_joc: StareJoc, heuristic, jucator_initial, jucator, max_depth=3, depth=3):
    # configuratie_tabla_rezultata = np.random.choice([-1, 0, 1], size=24)  # date de test random
    if depth <= 0:
        stare_joc.estimare = stare_joc.estimare_scor(depth, jucator_initial, heuristic)
        return stare_joc

    stari = []
    if jucator == stare_joc.JMIN and stare_joc.JMIN_num_piese < 9:
        stari = stari_posibile_pune_piese(stare_joc, jucator, max_depth, depth)
    elif jucator == stare_joc.JMAX and stare_joc.JMAX_num_piese < 9:
        stari = stari_posibile_pune_piese(stare_joc, jucator, max_depth, depth)
    else:
        stari = stari_posibile_muta_piese(stare_joc, jucator, max_depth, depth)

    mutari_cu_estimare = [min_max_pune_piese(stare, heuristic, jucator_initial, -jucator, max_depth, depth - 1) for stare in stari]

    # print("AI MOVE")
    if jucator == jucator_initial:
        # daca jucatorul este JMAX aleg estimarea maxima
        best_estimare = max(mutari_cu_estimare, key=lambda x: x.estimare).estimare
        best_mutari = [mutare for mutare in mutari_cu_estimare if mutare.estimare == best_estimare]
        best_move = random.choice(best_mutari)
    else:
        best_estimare = min(mutari_cu_estimare, key=lambda x: x.estimare).estimare
        best_mutari = [mutare for mutare in mutari_cu_estimare if mutare.estimare == best_estimare]
        best_move = random.choice(best_mutari)
    return best_move


def alpha_beta_pune_piesa(stare_joc: StareJoc, heuristic, jucator_initial, jucator, alpha, beta, max_depth=3, depth=3):
    if depth <= 0:
        stare_joc.estimare = stare_joc.estimare_scor(depth, jucator_initial, heuristic)
        return stare_joc

    if alpha > beta:
        return stare_joc  # este intr-un interval valid deci nu o mai procesez

    stari = []
    if jucator == stare_joc.JMIN and stare_joc.JMIN_num_piese < 9:
        stari = stari_posibile_pune_piese(stare_joc, jucator, max_depth, depth)
    elif jucator == stare_joc.JMAX and stare_joc.JMAX_num_piese < 9:
        stari = stari_posibile_pune_piese(stare_joc, jucator, max_depth, depth)
    else:
        stari = stari_posibile_muta_piese(stare_joc, jucator, max_depth, depth)

    best_move = []

    if jucator == jucator_initial:
        estimare_curenta = float('-inf')

        for mutare in stari:
            # calculez estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta_pune_piesa(stare_joc=mutare, jucator_initial=jucator_initial, jucator=-jucator,
                                               alpha=alpha, beta=beta, max_depth=max_depth, depth=depth-1,
                                               heuristic=heuristic)

            if stare_noua.estimare == estimare_curenta:
                best_move.append(stare_noua)

            if estimare_curenta < stare_noua.estimare:
                best_move = [stare_noua]
                estimare_curenta = stare_noua.estimare

            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif jucator == -jucator_initial:
        estimare_curenta = float('inf')

        for mutare in stari:
            stare_noua = alpha_beta_pune_piesa(stare_joc=mutare, jucator_initial=jucator_initial, jucator=-jucator,
                                               alpha=alpha, beta=beta, max_depth=max_depth, depth=depth - 1,
                                               heuristic=heuristic)

            if stare_noua.estimare == estimare_curenta:
                best_move.append(stare_noua)

            if estimare_curenta > stare_noua.estimare:
                best_move = [stare_noua]
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    if len(best_move) == 0:
        return stare_joc

    return random.choice(best_move)


def alpha_beta_muta_piesa(stare_joc: StareJoc, heuristic, jucator_initial, jucator, alpha, beta, max_depth=3, depth=3):
    if depth <= 0:
        stare_joc.estimare = stare_joc.estimare_scor(depth, jucator_initial, heuristic)
        return stare_joc

    if alpha > beta:
        return stare_joc

    stari = stari_posibile_muta_piese(stare_joc, jucator, max_depth, depth)
    best_move = []

    if jucator == stare_joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stari:
            stare_noua = alpha_beta_muta_piesa(stare_joc=mutare, jucator_initial=jucator_initial, jucator=-jucator,
                                               alpha=alpha, beta=beta, max_depth=max_depth, depth=depth-1,
                                               heuristic=heuristic)

            if stare_noua.estimare == estimare_curenta:
                best_move.append(stare_noua)

            if estimare_curenta < stare_noua.estimare:
                best_move = [stare_noua]
                estimare_curenta = stare_noua.estimare

            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif jucator == stare_joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stari:
            stare_noua = alpha_beta_muta_piesa(stare_joc=mutare, jucator_initial=jucator_initial, jucator=-jucator,
                                               alpha=alpha, beta=beta, max_depth=max_depth, depth=depth-1,
                                               heuristic=heuristic)

            if stare_noua.estimare == estimare_curenta:
                best_move.append(stare_noua)

            if estimare_curenta > stare_noua.estimare:
                best_move = [stare_noua]
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    if len(best_move) == 0:
        return stare_joc

    return random.choice(best_move)


def stari_posibile_pune_piese(stare_joc_parinte, jucator, max_depth, depth):
    configuratii_posibile = []
    piese_tabla = stare_joc_parinte.piese_tabla
    JMIN_piese = stare_joc_parinte.JMIN_num_piese
    JMAX_piese = stare_joc_parinte.JMAX_num_piese

    if depth == max_depth:
        stare_joc_parinte = None

    for index, valoare in enumerate(piese_tabla):
        if valoare == 0:
            aux_piese_tabla = copy.deepcopy(piese_tabla)
            aux_piese_tabla[index] = jucator

            stare_noua = StareJoc(tabla=aux_piese_tabla, GUI=False, parinte=stare_joc_parinte, index_move=index)
            stare_noua.JMIN_num_piese = JMIN_piese
            stare_noua.JMAX_num_piese = JMAX_piese

            if jucator == stare_noua.JMIN:
                stare_noua.JMIN_num_piese += 1
            elif jucator == stare_noua.JMAX:
                stare_noua.JMAX_num_piese += 1

            configuratii_posibile.append(stare_noua)

    return configuratii_posibile


def stari_posibile_muta_piese(stare_joc_parinte, jucator, max_depth, depth):
    configuratii_posibile = []
    piese_tabla = stare_joc_parinte.piese_tabla
    aux_stare_joc_parinte = StareJoc(stare_joc_parinte.piese_tabla, False, None)
    if depth == max_depth:
        stare_joc_parinte = None

    for index, valoare in enumerate(piese_tabla):
        if valoare == jucator:
            mutari_piesa = aux_stare_joc_parinte.vecinatati_libere(index)
            for mutare in mutari_piesa:
                # if mutare != -1 and piese_tabla[mutare] == 0:
                aux_piese_tabla = copy.deepcopy(piese_tabla)
                aux_piese_tabla[index] = 0
                aux_piese_tabla[mutare] = jucator
                configuratii_posibile.append(
                    StareJoc(tabla=aux_piese_tabla, GUI=False, parinte=stare_joc_parinte, index_move=mutare)
                )
    return configuratii_posibile


def indepartare_piesa(stare_joc: StareJoc, jucator):
    jucator *= -1
    # piesa adversarului eliminata va fi in urmatoarea ordine:
    # 1.daca sunt 2 piese aproape sa faca o moara
    # 2.o piesa singuratica
    # 3.o piesa random pentru ca toate piesele formeaza o moara

    categorii = []  # lista cu categoriile fiacarei piese si -1 pt spatiu si piesa gresita

    # 1. daca sunt 2 piese aproape sa faca o moara
    for index, piesa in enumerate(stare_joc.piese_tabla):
        if piesa == jucator:
            if stare_joc.doua_din_trei(index, jucator):
                # print("removed by categ1")
                stare_joc.piese_tabla[index] = 0
                return stare_joc

    # daca piesa este in moara, treci peste si cauta alta piesa
    # 0 -> pozitia este goala
    # 1 -> piesa este intr-o moara
    # 2 -> piesa pe care sa o scoatem
    for index, piesa in enumerate(stare_joc.piese_tabla):
        if piesa == jucator:
            if stare_joc.check_moara(index, jucator):
                categorii.append(3)
            else:
                categorii.append(2)
                stare_joc.piese_tabla[index] = 0
                # print("removed by categ2")
                return stare_joc
        else:
            categorii.append(0)

    try:
        first_index = categorii.index(3)
        stare_joc.piese_tabla[first_index] = 0
        return stare_joc
    except:
        pass

    try:
        first_index = categorii.index(2)
        stare_joc.piese_tabla[first_index] = 0
        # print("removed by categ2")
        return stare_joc
    except:
        first_index = np.where(stare_joc.piese_tabla == jucator)[0]
        stare_joc.piese_tabla[first_index] = 0
        return stare_joc



def piese_adversar(stare_joc, jucator):
    indecsi_piesa = []
    for index, piesa in enumerate(stare_joc.piese_tabla):
        if piesa == -jucator:
            indecsi_piesa.append(index)
    return indecsi_piesa


def stari_posibile_eliminare_piesa(stare_joc, jucator):
    configuratii_posibile = []
    piese_tabla = stare_joc.piese_tabla

    for index, valoare in enumerate(piese_tabla):
        if valoare == -jucator:
            aux_piese_tabla = copy.deepcopy(piese_tabla)
            aux_piese_tabla[index] = 0
            configuratii_posibile.append(
                StareJoc(tabla=aux_piese_tabla, GUI=False, parinte=stare_joc)
            )
    return configuratii_posibile

