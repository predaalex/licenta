import sys
import pygame
import board
import traditional_ai

joc = board.StareJoc()
ai_depth = 5

# consideram ca player1 ( JMIN este cel care incepe )
jucator = joc.JMIN


def ai_muta_piesa():
    global urmatoarea_stare, urmatoarea_stare
    # returneaza starea viitoare aleasa de min max
    # urmatoarea_stare = traditional_ai.min_max_muta_piese(stare_joc=joc,
    #                                                      jucator_initial=jucator, jucator=jucator,
    #                                                      max_depth=ai_depth, depth=ai_depth)
    urmatoarea_stare = traditional_ai.alpha_beta_muta_piesa(stare_joc=joc,
                                                            jucator_initial=jucator, jucator=jucator,
                                                            max_depth=ai_depth, depth=ai_depth,
                                                            alpha=-2000, beta=2000)
    while urmatoarea_stare.parinte is not None:
        urmatoarea_stare = urmatoarea_stare.parinte
    # urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
    #                             urmatoarea_stare.estimare_scor(0, joc.JMIN)
    # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
    # print(f"index_next_move = {urmatoarea_stare.index_move}") # DEBUG
    # Daca ai-ul face o moara, sa elimine o piese a adversarului
    if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
        print("ai-ul a facut o moara BLANA")  # DEBUG
        # if urmatoarea_stare.estimare - joc.estimare > 0:
        #     print("ai-ul a facut o moara")  # DEBUG
        joc.JMIN_num_piese -= 1

        urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
    joc.piese_tabla = urmatoarea_stare.piese_tabla
    print("ai-ul a mutat o piesa")


def ai_pune_piesa():
    global urmatoarea_stare, urmatoarea_stare
    # urmatoarea_stare = traditional_ai.min_max_pune_piese(stare_joc=joc,
    #                                                      jucator_initial=jucator, jucator=jucator,
    #                                                      max_depth=ai_depth, depth=ai_depth)

    urmatoarea_stare = traditional_ai.alpha_beta_pune_piesa(stare_joc=joc,
                                                            jucator_initial=jucator, jucator=jucator,
                                                            max_depth=ai_depth, depth=ai_depth,
                                                            alpha=-2000, beta=2000)

    # print(urmatoarea_stare) DEBUG
    while urmatoarea_stare.parinte is not None:
        urmatoarea_stare = urmatoarea_stare.parinte
    print("ai-ul a pus o piesa")
    # urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
    #                             urmatoarea_stare.estimare_scor(0, joc.JMIN)
    # print(urmatoarea_stare.piese_tabla) # DEBUG
    # print(urmatoarea_stare.estimare) # DEBUG
    # calculez scorul starii actuale, iar daca acesta fluctueaza ( +-2/3 ) unul dintre jucatori face o moara
    # joc.estimare = joc.estimare_scor(0, joc.JMAX) - joc.estimare_scor(0, joc.JMIN)
    # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
    # Daca ai-ul face o moara, sa elimine o piese a adversarului
    if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
        print("ai-ul a facut o moara BLANA")  # DEBUG
        # if urmatoarea_stare.estimare - joc.estimare > 0:
        #     print("ai-ul a facut o moara")  # DEBUG
        joc.JMIN_num_piese -= 1

        urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
    joc.piese_tabla = urmatoarea_stare.piese_tabla


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
            ai_pune_piesa()
            jucator *= -1

    print("Jucatorii trebuie sa isi mute piesele pe tabla")
    # in a doua faza a jocului, cei doi jucatori muta piesele pana cand unul dintre ei castiga
    jmin_win = False
    jmax_win = False
    first_move = True
    while True:
        if jucator == joc.JMIN:
            if first_move:
                jmin_win = joc.check_castigator(joc.JMIN)
                if jmin_win:
                    break
                first_move = False
            print('-------- 1st PLAYER TURN --------')
            # print(str(joc))
            joc.muta_piesa(jucator)
            jmin_win = joc.check_castigator(joc.JMIN)
            # print(f"jmin win check:{jmin_win}")  # DEBUG
            # print(f"nr_piese_jmax = {joc.JMAX_num_piese}") # DEBUG

            if jmin_win:
                break
            jucator *= -1
        elif jucator == joc.JMAX:
            print('-------- 2st PLAYER TURN --------')
            # print(str(joc))

            ai_muta_piesa()
            jmax_win = joc.check_castigator(joc.JMAX)
            # print(f"jmax_win_check:{jmax_win}")  # DEBUG
            if jmax_win:
                break
            jucator *= -1

        # print(f"nr_piese_jmin = {joc.JMIN_num_piese}")

    if jmin_win:
        print('--------- 1st PLAYER WON ------------')
    elif jmax_win:
        print('--------- 2st PLAYER WON ------------')
    else:
        print('ERROR -> nobody should win')

except KeyboardInterrupt:
    print("human_vs_ai interrupted")
    pygame.quit()
    sys.exit(0)
