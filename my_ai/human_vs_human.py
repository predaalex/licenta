import sys
import pygame
import board

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
            # print(str(joc))
            joc.pune_piesa(jucator)
            jucator *= -1

    print("Jucatorii trebuie sa isi mute piesele pe tabla")
    first_move = True
    # in a doua faza a jocului, cei doi jucatori muta piesele pana cand unul dintre ei castiga
    while not joc.check_castigator(-jucator):
        print(f"check:{joc.check_castigator(-jucator)} -> {-jucator}")
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
            # print(str(joc))
            joc.muta_piesa(jucator)
            jucator *= -1
        elif jucator == joc.JMAX:
            print('-------- 2st PLAYER TURN --------')
            # print(str(joc))
            joc.muta_piesa(jucator)
            jucator *= -1

    if jucator == joc.JMIN:
        print('--------- 1st PLAYER WON ------------')
    else:
        print('--------- 2st PLAYER WON ------------')

except KeyboardInterrupt:
    print("human_vs_human interrupted")
    pygame.quit()
    sys.exit(0)
