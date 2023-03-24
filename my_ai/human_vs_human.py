import sys
import pygame
import board

joc = board.StareJoc()
end = False
counter = 0
try:
    while not end:
        print()
        print('-------- 1st PLAYER TURN --------')
        # print(str(joc))
        # joc.pune_piesa(joc.JMIN)

        counter += 1

        joc.muta_piesa(joc.JMIN)

        if counter > 10:
            end = True
except KeyboardInterrupt:
    print("human_vs_human interrupted")
    pygame.quit()
    sys.exit(0)
