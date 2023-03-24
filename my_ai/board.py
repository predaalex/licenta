import sys
import time

import numpy as np
import pygame
from threading import Thread
from threading import Event
from time import sleep

GUI = True
x_click = 0
y_click = 0
click_settings = Event()

# global x_click, y_click, click_settings

# referinta la ce piese din array-ul piese_tabla au deasupra lor
above_arr = [-1, -1, -1,  # linia 1 de piese
             -1, 1, -1,  # linia 2
             -1, 4, -1,  # linia 3
             0, 3, 6, 8, 5, 2,  # linia 4
             11, -1, 12,  # linia 5
             10, 16, 13,  # linia 6
             9, 19, 14]  # linia 7
# coordonatele pieselor pe tabla(1, 7, 13 pentru ca este adaugata si spatierea
coord_arr = np.array([(1, 1), (7, 1), (13, 1),
                      (3, 3), (7, 3), (11, 3),
                      (5, 5), (7, 5), (9, 5),
                      (1, 7), (3, 7), (5, 7),   (9, 7), (11, 7), (13, 7),
                      (5, 9), (7, 9), (9, 9),
                      (3, 11), (7, 11), (11, 11),
                      (1, 13), (7, 13), (13, 13)],
                     dtype=[('x', 'i4'), ('y', 'i4')])


class StareJoc:
    def __init__(self):
        self.piese_tabla = None
        self.JMAX_num_piese = None
        self.JMIN_num_piese = None
        self.window = None
        self.clock = None
        self.reset()
        if GUI:
            self.init_GUI()

    def reset(self):
        # self.piese_tabla = np.zeros(24)  # zero inseamna ca nu este piesa
        self.piese_tabla = np.random.choice([-1, 0, 1], size=24) # date de test random
        self.JMIN_num_piese = 9  # numarul de piese al jucatorului
        self.JMAX_num_piese = 9

    def init_GUI(self):
        # Facem threadul care tine tabla updatata
        threading = Thread(target=self.update_gui)
        threading.start()

    def update_gui(self):
        global x_click, y_click, click_settings
        end = False

        # Initializam jocul
        pygame.init()
        self.window = pygame.display.set_mode(size=(700, 700))
        pygame.display.set_caption("Tintar -> Preda Alexandru-Florin")
        self.window.fill((160, 160, 150))  # culoarea de fundal al tablei
        self.clock = pygame.time.Clock()  # folosim pentru a seta refresh rate-ul

        while not end:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x_click, y_click = pygame.mouse.get_pos()
                        print(f"x = {x_click} || y = {y_click}")
                        click_settings.set()
                    elif event.type == pygame.QUIT:
                        end = True
                        # pygame.quit()
                        # sys.exit(0)

                    # desenam detaliile tablei(fundalul, liniiile intre pozitiile pieselor si piesele
                    self.desenare_tabla()
                    # updatam imaginea
                    pygame.display.flip()
                    # setam refresh rate-ul
                    self.clock.tick(60)
            except pygame.event:
                sys.exit(0)
        pygame.quit()
        sys.exit(0)

    def desenare_tabla(self):
        # 700 / 14 (13 coloane) = 50
        scala_imaginii = 50
        culoare_jucator1 = (50, 140, 50)
        culoare_jucator2 = (30, 30, 90)
        self.window.fill((160, 160, 150))  # culoarea de fundal al tablei
        # trasam liniile intre pozitiile pieselor
        # primul rand de linii exteriorare
        self.trage_linie([1, 1], [13, 1])
        self.trage_linie([1, 1], [1, 13])
        self.trage_linie([13, 1], [13, 13])
        self.trage_linie([1, 13], [13, 13])
        # al doilea rand de linii
        self.trage_linie([3, 3], [11, 3])
        self.trage_linie([3, 3], [3, 11])
        self.trage_linie([11, 3], [11, 11])
        self.trage_linie([3, 11], [11, 11])
        # randul interior
        self.trage_linie([5, 5], [9, 5])
        self.trage_linie([5, 5], [5, 9])
        self.trage_linie([5, 9], [9, 9])
        self.trage_linie([9, 5], [9, 9])
        # celelalte conexiuni
        self.trage_linie([1, 7], [5, 7])
        self.trage_linie([7, 1], [7, 5])
        self.trage_linie([13, 7], [9, 7])
        self.trage_linie([7, 13], [7, 9])



        # punem piesele pe tabla
        for i in range(0, len(self.piese_tabla)):
            # verificam daca exista piesa
            if self.piese_tabla[i] != 0:
                # pozitia in imagine
                centrul_pozitiei = [coord_arr['x'][i], coord_arr['y'][i]]
                # verificam cui ii apartine piesa si o desena
                if self.piese_tabla[i] > 0:
                    pygame.draw.circle(surface=self.window, color=culoare_jucator1,
                                       center=[x * scala_imaginii for x in centrul_pozitiei],
                                       radius=25)
                else:
                    pygame.draw.circle(surface=self.window, color=culoare_jucator2,
                                       center=[x * scala_imaginii for x in centrul_pozitiei],
                                       radius=25)

    def trage_linie(self, start, end, culoare_linii=(0, 0, 0), scala_imaginii=50, grosimea_liniei=8):
        pygame.draw.line(surface=self.window, color=culoare_linii,
                         start_pos= [x * scala_imaginii for x in start],
                         end_pos=   [x * scala_imaginii for x in end],
                         width=grosimea_liniei)


game = StareJoc()

