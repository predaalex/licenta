import sys
import PySimpleGUI as sg
import numpy as np
import pygame
import board
import traditional_ai
import time


def HumanVsAI():
    global joc, ai_depth_put, ai_depth_move, jucator, urmatoarea_stare
    print("START Human vs AI")
    joc = board.StareJoc()
    if joc.end:
        print("--------ENND-----------")
    # consideram ca player1 ( JMIN este cel care incepe )
    jucator = joc.JMIN

    def ai_muta_piesa():
        global urmatoarea_stare, urmatoarea_stare
        # returneaza starea viitoare aleasa de min max
        urmatoarea_stare = traditional_ai.min_max_muta_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_move, depth=ai_depth_move)
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMIN)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # print(f"index_next_move = {urmatoarea_stare.index_move}") # DEBUG
        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara ")  # DEBUG
            # if urmatoarea_stare.estimare - joc.estimare > 0:
            #     print("ai-ul a facut o moara")  # DEBUG
            joc.JMIN_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla
        print("ai-ul a mutat o piesa")

    def ai_pune_piesa(ai_depth_put, joc, jucator):
        global urmatoarea_stare
        # returneaza starea viitoare aleasa de min max
        urmatoarea_stare = traditional_ai.min_max_pune_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_put, depth=ai_depth_put)
        # print(urmatoarea_stare) DEBUG
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        print("ai-ul a pus o piesa")
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMIN)
        # print(urmatoarea_stare.piese_tabla) # DEBUG
        # print(urmatoarea_stare.estimare) # DEBUG
        # calculez scorul starii actuale, iar daca acesta fluctueaza ( +-2/3 ) unul dintre jucatori face o moara
        joc.estimare = joc.estimare_scor(0, joc.JMAX) - joc.estimare_scor(0, joc.JMIN)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara ")  # DEBUG
            # if urmatoarea_stare.estimare - joc.estimare > 0:
            #     print("ai-ul a facut o moara")  # DEBUG
            joc.JMIN_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla

    try:
        # in prima faza a jocului, fiecare jucator isi pozitioneaza cele 9 piese
        print("Jucatorii trebuie sa isi plaseze piesele pe tabla")
        for i in range(18):
            if jucator == joc.JMIN and not joc.end:
                print('-------- 1st PLAYER TURN --------')
                joc.pune_piesa(jucator)
                jucator *= -1
            elif jucator == joc.JMAX and not joc.end:
                print('-------- 2st PLAYER TURN --------')

                ai_pune_piesa(ai_depth_put, joc, jucator)
                jucator *= -1
        if not joc.end:
            print("Jucatorii trebuie sa isi mute piesele pe tabla")
        # in a doua faza a jocului, cei doi jucatori muta piesele pana cand unul dintre ei castiga
        jmin_win = False
        jmax_win = False
        first_move = True
        while True and not joc.end:

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
            print('ERROR -> nobody should win || game ended sooner')

    except KeyboardInterrupt:
        print("human_vs_ai interrupted")
        pygame.quit()


def HumanVsHuman():
    global joc, jucator
    print("START Human vs Human")
    joc = board.StareJoc()
    if joc.end:
        print("--------ENND-----------")
    # consideram ca player1 ( JMIN este cel care incepe )
    jucator = joc.JMIN
    try:
        # in prima faza a jocului, fiecare jucator isi pozitioneaza cele 9 piese
        print("Jucatorii trebuie sa isi plaseze piesele pe tabla")
        for i in range(18):
            if jucator == joc.JMIN and not joc.end:
                print('-------- 1st PLAYER TURN --------')
                # print(str(joc))
                joc.pune_piesa(jucator)
                jucator *= -1
            elif jucator == joc.JMAX and not joc.end:
                print('-------- 2st PLAYER TURN --------')
                # print(str(joc))
                joc.pune_piesa(jucator)
                jucator *= -1

        if not joc.end:
            print("Jucatorii trebuie sa isi mute piesele pe tabla")
        jmin_win = False
        jmax_win = False
        first_move = True
        # in a doua faza a jocului, cei doi jucatori muta piesele pana cand unul dintre ei castiga
        while True and not joc.end:
            # print(f"check:{joc.check_castigator(-jucator)} -> {-jucator}") # DEBUG
            if jucator == joc.JMIN:
                if first_move:
                    jmin_win = joc.check_castigator(joc.JMIN)
                    if jmin_win:
                        break
                    jmax_win = joc.check_castigator(joc.JMAX)
                    if jmax_win:
                        break
                    first_move = False
                print('-------- 1st PLAYER TURN --------')
                joc.muta_piesa(jucator)
                jmin_win = joc.check_castigator(joc.JMIN)
                if jmin_win:
                    break
                jucator *= -1
            elif jucator == joc.JMAX:
                print('-------- 2st PLAYER TURN --------')
                joc.muta_piesa(jucator)
                jmax_win = joc.check_castigator(joc.JMAX)
                if jmax_win:
                    break
                jucator *= -1

        if jmin_win:
            print('--------- 1st PLAYER WON ------------')
        elif jmax_win:
            print('--------- 2st PLAYER WON ------------')
        else:
            print('ERROR -> nobody should win || game ended sooner')

    except KeyboardInterrupt:
        print("human_vs_human interrupted")
        pygame.quit()


def AIVsAI():
    global joc, ai_depth_put, ai_depth_move, jucator
    joc = board.StareJoc(GUI=True)
    game_time = time.time()
    move_time = None
    # consideram ca player1 ( JMIN este cel care incepe )
    jucator = joc.JMIN

    def ai1_pune_piesa():
        global move_time, urmatoarea_stare, urmatoarea_stare
        move_time = time.time()

        urmatoarea_stare = traditional_ai.min_max_pune_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_put, depth=ai_depth_put)
        # print(urmatoarea_stare) DEBUG
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        print("ai-ul a pus o piesa")
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMIN) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMAX)
        # print(urmatoarea_stare.piese_tabla) # DEBUG
        # print(urmatoarea_stare.estimare) # DEBUG
        # calculez scorul starii actuale, iar daca acesta fluctueaza ( +-2/3 ) unul dintre jucatori face o moara
        joc.estimare = joc.estimare_scor(0, joc.JMIN) - joc.estimare_scor(0, joc.JMAX)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara ")  # DEBUG
            # if urmatoarea_stare.estimare - joc.estimare > 0:
            #     print("ai-ul a facut o moara")  # DEBUG
            joc.JMAX_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla
        print(f"mutarea a durat:{time.time() - move_time} s")

    def ai2_pune_piesa():
        global move_time, urmatoarea_stare, urmatoarea_stare
        move_time = time.time()

        # returneaza starea viitoare aleasa de min max
        urmatoarea_stare = traditional_ai.min_max_pune_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_put, depth=ai_depth_put)
        # print(urmatoarea_stare) DEBUG
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        print("ai-ul a pus o piesa")
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMIN)
        # print(urmatoarea_stare.piese_tabla) # DEBUG
        # print(urmatoarea_stare.estimare) # DEBUG
        # calculez scorul starii actuale, iar daca acesta fluctueaza ( +-2/3 ) unul dintre jucatori face o moara
        joc.estimare = joc.estimare_scor(0, joc.JMAX) - joc.estimare_scor(0, joc.JMIN)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara ")  # DEBUG
            # if urmatoarea_stare.estimare - joc.estimare > 0:
            #     print("ai-ul a facut o moara")  # DEBUG
            joc.JMIN_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla
        print(f"mutarea a durat:{time.time() - move_time} s")

    def ai1_muta_piesa():
        global move_time, urmatoarea_stare, urmatoarea_stare
        move_time = time.time()
        # print(str(joc))
        # returneaza starea viitoare aleasa de min max
        urmatoarea_stare = traditional_ai.min_max_muta_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_move, depth=ai_depth_move)
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMIN) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMAX)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # print(f"index_next_move = {urmatoarea_stare.index_move}") # DEBUG
        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara ")  # DEBUG
            # if urmatoarea_stare.estimare - joc.estimare > 0:
            #     print("ai-ul a facut o moara")  # DEBUG
            joc.JMAX_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla

        print(f"mutarea a durat:{time.time() - move_time} s")

    def ai2_muta_piesa():
        global move_time, urmatoarea_stare, urmatoarea_stare
        move_time = time.time()
        # print(str(joc))
        # returneaza starea viitoare aleasa de min max
        urmatoarea_stare = traditional_ai.min_max_muta_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_move, depth=ai_depth_move)
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMIN)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # print(f"index_next_move = {urmatoarea_stare.index_move}") # DEBUG

        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara")  # DEBUG
            joc.JMIN_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla
        print("ai-ul a mutat o piesa")
        print(f"mutarea a durat:{time.time() - move_time} s")

    try:
        # in prima faza a jocului, fiecare jucator isi pozitioneaza cele 9 piese
        print("Jucatorii trebuie sa isi plaseze piesele pe tabla")
        for i in range(18):
            if jucator == joc.JMIN and not joc.end:
                print('-------- 1st PLAYER TURN --------')
                ai1_pune_piesa()
                jucator *= -1
            elif jucator == joc.JMAX and not joc.end:
                print('-------- 2st PLAYER TURN --------')
                ai2_pune_piesa()
                jucator *= -1
        if not joc.end:
            print("Jucatorii trebuie sa isi mute piesele pe tabla")
        # in a doua faza a jocului, cei doi jucatori muta piesele pana cand unul dintre ei castiga
        jmin_win = False
        jmax_win = False
        first_move = True
        numar_mutari = 0
        while True and not joc.end:
            if jucator == joc.JMIN:
                if first_move:
                    jmin_win = joc.check_castigator(joc.JMIN)
                    if jmin_win:
                        break
                    first_move = False
                print('-------- 1st PLAYER TURN --------')
                ai1_muta_piesa()
                numar_mutari += 1

                jmin_win = joc.check_castigator(joc.JMIN)
                if jmin_win:
                    break

                jucator *= -1

            elif jucator == joc.JMAX:
                print('-------- 2st PLAYER TURN --------')

                ai2_muta_piesa()
                numar_mutari += 1


                jmax_win = joc.check_castigator(joc.JMAX)
                if jmax_win:
                    break

                jucator *= -1

            print(f"numar piese jmax = {joc.JMAX_num_piese}")
            print(f"numar piese jmin = {joc.JMIN_num_piese}")

        if jmin_win:
            print('--------- 1st PLAYER WON ------------')
        elif jmax_win:
            print('--------- 2st PLAYER WON ------------')
        else:
            print('ERROR -> nobody should win')

        if joc.end:
            print("--------ENND-----------")

        print(f"Jocul a durat:{time.time() - game_time} s")
        print(f"Jocul a avut:{numar_mutari + 18} numar mutari")

    except KeyboardInterrupt:
        print("ai_vs_ai interrupted")
        pygame.quit()


def HumanVsAI_Camera():
    global jucator, ai_depth_move, ai_depth_put, joc
    # Initializare Pygame
    joc = board.StareJoc(camera=True)
    # consideram ca player1 ( JMIN este cel care incepe )
    jucator = joc.JMIN

    def ai_muta_piesa():
        global urmatoarea_stare, urmatoarea_stare
        # returneaza starea viitoare aleasa de min max
        urmatoarea_stare = traditional_ai.min_max_muta_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_move, depth=ai_depth_move)
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMIN)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # print(f"index_next_move = {urmatoarea_stare.index_move}") # DEBUG
        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if not joc.end and urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara ")  # DEBUG
            # if urmatoarea_stare.estimare - joc.estimare > 0:
            #     print("ai-ul a facut o moara")  # DEBUG
            joc.JMIN_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla
        print("ai-ul a mutat o piesa")

    def ai_pune_piesa():
        global urmatoarea_stare, urmatoarea_stare
        # returneaza starea viitoare aleasa de min max
        urmatoarea_stare = traditional_ai.min_max_pune_piese(stare_joc=joc,
                                                             jucator_initial=jucator, jucator=jucator,
                                                             max_depth=ai_depth_put, depth=ai_depth_put)
        # print(urmatoarea_stare) DEBUG
        while urmatoarea_stare.parinte is not None:
            urmatoarea_stare = urmatoarea_stare.parinte
        print("ai-ul a pus o piesa")
        urmatoarea_stare.estimare = urmatoarea_stare.estimare_scor(0, joc.JMAX) - \
                                    urmatoarea_stare.estimare_scor(0, joc.JMIN)
        # print(urmatoarea_stare.piese_tabla) # DEBUG
        # print(urmatoarea_stare.estimare) # DEBUG
        # calculez scorul starii actuale, iar daca acesta fluctueaza ( +-2/3 ) unul dintre jucatori face o moara
        joc.estimare = joc.estimare_scor(0, joc.JMAX) - joc.estimare_scor(0, joc.JMIN)
        # print(f"joc = {joc.estimare} urm_stare = {urmatoarea_stare.estimare}")  # DEBUG
        # Daca ai-ul face o moara, sa elimine o piese a adversarului
        if not joc.end and urmatoarea_stare.check_moara(urmatoarea_stare.index_move, jucator):
            print("ai-ul a facut o moara ")  # DEBUG
            # if urmatoarea_stare.estimare - joc.estimare > 0:
            #     print("ai-ul a facut o moara")  # DEBUG
            joc.JMIN_num_piese -= 1

            urmatoarea_stare = traditional_ai.indepartare_piesa(urmatoarea_stare, jucator)
        joc.piese_tabla = urmatoarea_stare.piese_tabla

    def jucator_pune_piesa():
        global configuratie_valida, configuratie_camera, stari_posibile, index_mutare, stare, joc
        # punem piesa
        configuratie_valida = False
        configuratie_camera = []
        print(joc)
        stari_posibile = traditional_ai.stari_posibile_pune_piese(joc, jucator, 1, 1)
        index_mutare = -1
        while not configuratie_valida:
            configuratie_camera = board.get_configuratie_camera()
            for stare in stari_posibile:
                if np.array_equal(stare.piese_tabla, configuratie_camera):
                    configuratie_valida = True
                    index_mutare = stare.index_move
                    break

            if configuratie_valida:
                configuratie_valida = False
                break
            elif joc.end:
                break
            else:
                print("configuratia nu este valida, pune piesa corect")
        print("Piesa a fost pusa cu succes")
        joc.piese_tabla = configuratie_camera
        joc_aux = joc
        # verificam daca piesa pusa se afla intr-o moara
        if not joc.end and joc_aux.check_moara(index_mutare, jucator):
            print("piesa pusa formeaza o moara, indeparteaza o piesa a adversarului")
            # eliminam o piesa a adversarului
            while not configuratie_valida:
                configuratie_camera = board.get_configuratie_camera()
                stari_posibile = traditional_ai.stari_posibile_eliminare_piesa(joc_aux, jucator)

                for stare in stari_posibile:
                    if np.array_equal(stare.piese_tabla, configuratie_camera):
                        configuratie_valida = True
                        break

                if configuratie_valida:
                    break
                elif joc.end:
                    break
                else:
                    print("configuratia nu este valida, ia o singura piesa a adversarului")
            joc.JMAX_num_piese -= 1
        joc.piese_tabla = configuratie_camera

    def jucator_muta_piesa():
        global configuratie_valida, configuratie_camera, stari_posibile, index_mutare, stare, joc
        # muta piesa
        configuratie_valida = False
        configuratie_camera = []
        stari_posibile = traditional_ai.stari_posibile_muta_piese(joc, jucator, 1, 1)
        index_mutare = -1
        while not configuratie_valida:
            configuratie_camera = board.get_configuratie_camera()
            for stare in stari_posibile:
                if np.array_equal(stare.piese_tabla, configuratie_camera):
                    configuratie_valida = True
                    index_mutare = stare.index_move
                    break

            if configuratie_valida:
                configuratie_valida = False
                break
            elif joc.end:
                break
            else:
                print("configuratia nu este valida, muta piesa conform regulamentul jocului")
        print("Piesa a fost mutata cu succes")
        joc.piese_tabla = configuratie_camera
        joc_aux = joc
        # verificam daca piesa pusa se afla intr-o moara
        if not joc.end and joc_aux.check_moara(index_mutare, jucator):
            print("piesa pusa formeaza o moara, indeparteaza o piesa a adversarului")
            # eliminam o piesa a adversarului
            while not configuratie_valida:
                configuratie_camera = board.get_configuratie_camera()
                stari_posibile = traditional_ai.stari_posibile_eliminare_piesa(joc_aux, jucator)

                for stare in stari_posibile:
                    if np.array_equal(stare.piese_tabla, configuratie_camera):
                        configuratie_valida = True
                        break

                if configuratie_valida:
                    break
                elif joc.end:
                    break
                else:
                    print("configuratia nu este valida, ia o singura piesa a adversarului")
            joc.JMAX_num_piese -= 1
        joc.piese_tabla = configuratie_camera

    try:
        # in prima faza a jocului, fiecare jucator isi pozitioneaza cele 9 piese
        print("Jucatorii trebuie sa isi plaseze piesele pe tabla")
        for i in range(18):
            if jucator == joc.JMIN and not joc.end:
                print('-------- 1st PLAYER TURN --------')
                jucator_pune_piesa()

                jucator *= -1
            elif jucator == joc.JMAX and not joc.end:
                print('-------- 2st PLAYER TURN --------')
                ai_pune_piesa()
                jucator *= -1
        if not joc.end:
            print("Jucatorii trebuie sa isi mute piesele pe tabla")
        # in a doua faza a jocului, cei doi jucatori muta piesele pana cand unul dintre ei castiga
        jmin_win = False
        jmax_win = False
        first_move = True
        while True and not joc.end:
            if jucator == joc.JMIN:
                if first_move:
                    jmin_win = joc.check_castigator(joc.JMIN)
                    if jmin_win:
                        break
                    first_move = False
                print('-------- 1st PLAYER TURN --------')
                # print(str(joc))

                jucator_muta_piesa()

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

        if jmin_win:
            print('--------- 1st PLAYER WON ------------')
        elif jmax_win:
            print('--------- 2st PLAYER WON ------------')
        else:
            print('ERROR -> nobody should win || game ended sooner')

    except KeyboardInterrupt:
        print("human_vs_ai interrupted")
        pygame.quit()


class PyWindow:

    def __init__(self):
        self.window = None
        sg.theme("DarkAmber")
        self.create_window()

    def create_window(self):
        layout = self.create_window_layout()

        self.window = sg.Window("Tintar <=> Preda Alexandru-Florin", layout, no_titlebar=False)

    def create_window_layout(self):
        tab_group_layout = self.create_tabs()

        return [[sg.TabGroup(tab_group_layout,
                             enable_events=True,
                             key="-TABGROUP-")]]

    def create_tabs(self):
        tab1_layout = self.game_tab()
        tab2_layout = self.options_tab()

        tab1 = sg.Tab("GAME", tab1_layout, font="Courier 15", key="-TAB1-")
        tab2 = sg.Tab("OPTIONS", tab2_layout, font="Courier 15", key="-TAB2-")

        return [[tab1, tab2]]

    def game_tab(self):
        return [[sg.Text("Welcome to Nine Men's Morrys Game")],

                [sg.Frame("Select the type of game you want to play in PyGame",
                          [[sg.Button("Human vs Human", key="-HvsH-")],
                           [sg.Button("Human vs AI", key="-HvsAI-")],
                           [sg.Button("AI vs AI", key="-AIvsAI-")]]
                          )],
                [sg.Frame("Select the type of game you want to play using camera syncronization",
                          [[sg.Button("Human vs AI", key="-HvsAI_Camera-")]]
                          )]]

    def options_tab(self):
        return [[sg.Text("You can set the engine settings or it will use the default ones")],
                [sg.Frame("Min-Max parameters",
                          [[sg.Text("Depth of ai putting pieces"),
                            sg.Slider(range=(1, 7), key="-AI_DEPTH_PUT-", orientation='v', size=(5, 20),
                                      default_value=3),
                            sg.Text("Depth of ai moving pieces"),
                            sg.Slider(range=(1, 9), key="-AI_DEPTH_MOVE-", orientation='v', size=(5, 20),
                                      default_value=3)]]
                          )]]


window = PyWindow().window

while True:
    event, values = window.read(timeout=1)

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event != sg.TIMEOUT_KEY:
        ai_depth_put = values["-AI_DEPTH_PUT-"]
        ai_depth_move = values["-AI_DEPTH_MOVE-"]
        if event == "-HvsH-":
            HumanVsHuman()
        elif event == "-HvsAI-":
            HumanVsAI()
        elif event == "-AIvsAI-":
            AIVsAI()
        elif event == "-HvsAI_Camera-":
            HumanVsAI_Camera()

window.close()
sys.exit(0)
