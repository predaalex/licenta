import sys
import pygame
import board
import traditional_ai

joc = board.StareJoc()
end = False

# consideram ca player1 ( JMIN este cel care incepe )
jucator = joc.JMIN
try:
    # in prima faza a jocului, fiecare jucator isi pozitioneaza cele 9 piese
    print("Jucatorii trebuie sa isi plaseze piesele pe tabla")
    for i in range(18):
        print()
        if jucator == joc.JMIN:
            print('-------- 1st PLAYER TURN --------')
            # print(str(joc))
            joc.pune_piesa(jucator)
            jucator *= -1
        elif jucator == joc.JMAX:
            print('-------- 2st PLAYER TURN --------')
            # print(str(joc)) DEBUG

            # returneaza starea viitoare aleasa de min max
            urmatoarea_stare = traditional_ai.min_max_pune_piese(joc, jucator)
            # print(urmatoarea_stare) DEBUG
            while urmatoarea_stare.parinte is not None:
                urmatoarea_stare = urmatoarea_stare.parinte
            urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                        urmatoarea_stare.estimare_scor(0, joc.JMIN)

            # print(urmatoarea_stare.piese_tabla) # DEBUG
            # print(urmatoarea_stare.estimare) # DEBUG

            # calculez scorul starii actuale, iar daca acesta fluctueaza ( +-2/3 ) unul dintre jucatori face o moara

            joc.estimare = joc.estimare_scor(0, joc.JMAX) - joc.estimare_scor(0, joc.JMIN)

            print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG

            # Daca ai-ul face o moara, sa elimine o piese a adversarului
            if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
                print("ai-ul a facut o moara BLANA")  # DEBUG
                # if urmatoarea_stare.estimare - joc.estimare > 0:
                #     print("ai-ul a facut o moara")  # DEBUG
                joc.JMAX_num_piese -= 1

                urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)

            joc.piese_tabla = urmatoarea_stare.piese_tabla
            jucator *= -1

    print("Jucatorii trebuie sa isi mute piesele pe tabla")
    # in a doua faza a jocului, cei doi jucatori muta piesele pana cand unul dintre ei castiga
    while not joc.check_castigator(-jucator):
        print(f"check:{joc.check_castigator(jucator)} -> {jucator}")
        if jucator == joc.JMIN:
            print('-------- 1st PLAYER TURN --------')
            # print(str(joc))
            joc.muta_piesa(jucator)
            jucator *= -1
        elif jucator == joc.JMAX:
            print('-------- 2st PLAYER TURN --------')
            # print(str(joc))

            # returneaza starea viitoare aleasa de min max
            urmatoarea_stare = traditional_ai.min_max_muta_piese(joc, jucator)

            while urmatoarea_stare.parinte is not None:
                urmatoarea_stare = urmatoarea_stare.parinte

            urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                        urmatoarea_stare.estimare_scor(0, joc.JMIN)

            print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
            # print(f"index_next_move = {urmatoarea_stare.index_move}") # DEBUG
            # Daca ai-ul face o moara, sa elimine o piese a adversarului
            if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
                print("ai-ul a facut o moara BLANA")  # DEBUG
                # if urmatoarea_stare.estimare - joc.estimare > 0:
                #     print("ai-ul a facut o moara")  # DEBUG
                joc.JMAX_num_piese -= 1

                urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)

            joc.piese_tabla = urmatoarea_stare.piese_tabla
            jucator *= -1

    if jucator == joc.JMIN:
        print('--------- 1st PLAYER WON ------------')
    else:
        print('--------- 2st PLAYER WON ------------')

except KeyboardInterrupt:
    print("human_vs_human interrupted")
    pygame.quit()
    sys.exit(0)
