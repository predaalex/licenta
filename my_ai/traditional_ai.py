import copy

import board


def stari_posibile_pune_piese(stare_joc_parinte, jucator, depth):
    configuratii_posibile = []
    piese_tabla = stare_joc_parinte.piese_tabla

    if depth == 3:
        stare_joc_parinte = None

    for index, valoare in enumerate(piese_tabla):
        if valoare == 0:
            aux_piese_tabla = copy.deepcopy(piese_tabla)
            aux_piese_tabla[index] = jucator
            configuratii_posibile.append(
                board.StareJoc(tabla=aux_piese_tabla, GUI=False, parinte=stare_joc_parinte, index_move=index)
            )

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

    stari = stari_posibile_pune_piese(stare_joc, jucator, depth)
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


def doua_din_trei(stare_joc, index, jucator):
    index_piesa_dreapta = stare_joc.get_index_dreapta(index)
    index_piesa_dreapta_dreapta = stare_joc.get_index_dreapta(stare_joc.get_index_dreapta(index))
    index_piesa_stanga = stare_joc.get_index_stanga(index)
    index_piesa_stanga_stanga = stare_joc.get_index_stanga(stare_joc.get_index_stanga(index))
    index_piesa_sus = stare_joc.get_index_sus(index)
    index_piesa_sus_sus = stare_joc.get_index_sus(stare_joc.get_index_sus(index))
    index_piesa_jos = stare_joc.get_index_jos(index)
    index_piesa_jos_jos = stare_joc.get_index_jos(stare_joc.get_index_jos(index))

    # pe linie in colturi
    # stanga
    if index_piesa_stanga != -1 and stare_joc.piese_tabla[index_piesa_stanga] == jucator and \
            index_piesa_stanga_stanga != -1 and stare_joc.piese_tabla[index_piesa_stanga_stanga] == 0:
        return True
    # dreapta
    if index_piesa_dreapta != -1 and stare_joc.piese_tabla[index_piesa_dreapta] == jucator and \
            index_piesa_dreapta_dreapta != -1 and stare_joc.piese_tabla[index_piesa_dreapta_dreapta] == 0:
        return True
    # pe linie pe mijloc si stanga
    if index_piesa_stanga != -1 and stare_joc.piese_tabla[index_piesa_stanga] == jucator and \
            index_piesa_dreapta != -1 and stare_joc.piese_tabla[index_piesa_dreapta] == 0:
        return True
    # pe linie pe mijloc si dreapta
    if index_piesa_dreapta != - 1 and stare_joc.piese_tabla[index_piesa_dreapta] == jucator and \
            index_piesa_stanga != -1 and stare_joc.piese_tabla[index_piesa_stanga] == 0:
        return True
    # pe linie in colturi
    if index_piesa_dreapta != -1 and stare_joc.piese_tabla[index_piesa_dreapta] == 0 and \
            index_piesa_dreapta_dreapta != -1 and stare_joc.piese_tabla[index_piesa_dreapta_dreapta] == jucator:
        return True
    # pe linie in colturi
    if index_piesa_stanga != -1 and stare_joc.piese_tabla[index_piesa_stanga] == 0 and \
            index_piesa_stanga_stanga != -1 and stare_joc.piese_tabla[index_piesa_stanga_stanga] == jucator:
        return True

    # pe coloana in colturi
    # sus
    if index_piesa_jos != -1 and stare_joc.piese_tabla[index_piesa_jos] == jucator and \
            index_piesa_jos_jos != -1 and stare_joc.piese_tabla[index_piesa_jos_jos] == 0:
        return True
    # jos
    if index_piesa_sus != -1 and stare_joc.piese_tabla[index_piesa_sus] == jucator and \
            index_piesa_sus_sus != -1 and stare_joc.piese_tabla[index_piesa_sus_sus] == 0:
        return True
    # pe coloana pe mijloc si sus
    if index_piesa_sus != -1 and stare_joc.piese_tabla[index_piesa_sus] == jucator and \
            index_piesa_jos_jos != -1 and stare_joc.piese_tabla[index_piesa_jos_jos] == 0:
        return True
    # pe coloana pe mijloc si jos
    if index_piesa_jos != -1 and stare_joc.piese_tabla[index_piesa_jos] == jucator and \
            index_piesa_sus_sus != -1 and stare_joc.piese_tabla[index_piesa_sus_sus] == 0:
        return True
    # pe coloana sus si jos
    if index_piesa_sus != -1 and stare_joc.piese_tabla[index_piesa_sus] == 0 and \
            index_piesa_sus_sus != -1 and stare_joc.piese_tabla[index_piesa_sus_sus] == jucator:
        return True
    # pe coloana jos si sus
    if index_piesa_jos != -1 and stare_joc.piese_tabla[index_piesa_jos] == 0 and \
            index_piesa_jos_jos != -1 and stare_joc.piese_tabla[index_piesa_jos_jos] == jucator:
        return True

    return False


def indepartare_piesa(stare_joc: board.StareJoc, jucator):
    jucator *= -1
    # piesa adversarului eliminata va fi in urmatoarea ordine:
    # 1.daca sunt 2 piese aproape sa faca o moara
    # 2.o piesa singuratica
    # 3.o piesa random pentru ca toate piesele formeaza o moara

    categorii = []  # lista cu categoriile fiacarei piese si -1 pt spatiu si piesa gresita

    # 1. daca sunt 2 piese aproape sa faca o moara
    for index, piesa in enumerate(stare_joc.piese_tabla):
        if piesa == jucator:
            if doua_din_trei(stare_joc, index, jucator):
                print("removed by categ1")
                stare_joc.piese_tabla[index] = 0
                return stare_joc

    # daca piesa este in moara, treci peste si cauta alta piesa
    # 0 -> pozitia este goala
    # 1 -> piesa e intr-o moara
    # 2 -> piesa pe care sa o scoatem
    for index, piesa in enumerate(stare_joc.piese_tabla):
        if piesa == jucator:
            if stare_joc.check_moara(index, jucator):
                categorii.append(3)
            else:
                categorii.append(2)
        else:
            categorii.append(0)

    for index, categ in enumerate(categorii):
        if categ == 3:
            stare_joc.piese_tabla[index] = 0
            print("removed by categ3")
            return stare_joc

    first_index = categorii.index(2)
    stare_joc.piese_tabla[first_index] = 0
    print("removed by categ2")
    return stare_joc


def vecinatati_libere(stare_joc, index):
    index_piesa_dreapta = stare_joc.get_index_dreapta(index)
    index_piesa_stanga = stare_joc.get_index_stanga(index)
    index_piesa_sus = stare_joc.get_index_sus(index)
    index_piesa_jos = stare_joc.get_index_jos(index)

    vecini = []

    if index_piesa_stanga != -1 and stare_joc.piese_tabla[index_piesa_stanga] == 0:
        vecini.append(index_piesa_stanga)
    if index_piesa_dreapta != -1 and stare_joc.piese_tabla[index_piesa_dreapta] == 0:
        vecini.append(index_piesa_dreapta)
    if index_piesa_sus != -1 and stare_joc.piese_tabla[index_piesa_sus] == 0:
        vecini.append(index_piesa_sus)
    if index_piesa_jos != -1 and stare_joc.piese_tabla[index_piesa_jos] == 0:
        vecini.append(index_piesa_jos)

    stare_joc.pozitii_valide_mutare(index)

    return vecini


def stari_posibile_muta_piese(stare_joc_parinte, jucator, depth):
    configuratii_posibile = []
    piese_tabla = stare_joc_parinte.piese_tabla
    aux_stare_joc_parinte = board.StareJoc(stare_joc_parinte.piese_tabla, False, None)
    if depth == 3:
        stare_joc_parinte = None

    for index, valoare in enumerate(piese_tabla):
        if valoare == jucator:
            mutari_piesa = vecinatati_libere(aux_stare_joc_parinte, index)
            for mutare in mutari_piesa:
                # if mutare != -1 and piese_tabla[mutare] == 0:
                aux_piese_tabla = copy.deepcopy(piese_tabla)
                aux_piese_tabla[index] = 0
                aux_piese_tabla[mutare] = jucator
                configuratii_posibile.append(
                    board.StareJoc(tabla=aux_piese_tabla, GUI=False, parinte=stare_joc_parinte, index_move=mutare)
                )
    return configuratii_posibile


def min_max_muta_piese(stare_joc: board.StareJoc, jucator, depth=3):
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

    stari = stari_posibile_muta_piese(stare_joc, jucator, depth)
    # print(f"mutari posibile {len(stari)}\n")

    mutari_cu_estimare = [min_max_muta_piese(stare, -jucator, depth - 1) for stare in stari]
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
