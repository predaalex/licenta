import math
import sys

import numpy as np
import pygame
from threading import Thread
from threading import Event

x_click = 0
y_click = 0
click_event = Event()

# global x_click, y_click, click_settings

# referinta la ce piese din array-ul piese_tabla au deasupra lor(lookup table)
above_arr = [-1, -1, -1,  # linia 1 de piese
             -1,  1, -1,  # linia 2
             -1,  4, -1,  # linia 3
             0,   3,  6,   8, 5, 2,  # linia 4
             11, -1, 12,  # linia 5
             10, 16, 13,  # linia 6
             9,  19, 14]  # linia 7
# coordonatele pieselor pe tabla(1, 7, 13 pentru ca este adaugata si spatierea
coord_arr = np.array([(1, 1),  (7, 1),  (13, 1),
                      (3, 3),  (7, 3),  (11, 3),
                      (5, 5),  (7, 5),  (9,  5),
                      (1, 7),  (3, 7),  (5,  7), (9, 7), (11, 7), (13, 7),
                      (5, 9),  (7, 9),  (9,  9),
                      (3, 11), (7, 11), (11, 11),
                      (1, 13), (7, 13), (13, 13)],
                     dtype=[('x', 'i4'), ('y', 'i4')])


class StareJoc:
    def __init__(self, tabla=None, GUI=True, parinte=None, index_move=None):
        self.estimare = None
        self.raza_piesa = None
        self.culoare_jucator2 = None
        self.culoare_jucator1 = None
        self.scala_imaginii = None
        self.piese_tabla = None
        self.JMAX_num_piese = None
        self.JMIN_num_piese = None
        self.JMIN = -1
        self.JMAX = 1
        self.window = None
        self.clock = None
        self.parinte = parinte
        self.index_move = index_move
        self.reset(tabla)
        if GUI:
            self.init_GUI()

    def __str__(self):
        return self.afisare_tabla()

    def reset(self, tabla):
        if tabla is None:
            self.piese_tabla = np.zeros(24)  # zero inseamna ca nu este piesa
        else:
            self.piese_tabla = tabla
        # self.piese_tabla = np.random.choice([-1, 0, 1], size=24)  # date de test random
        self.JMIN_num_piese = 9  # numarul de piese al jucatorului
        self.JMAX_num_piese = 9

    def init_GUI(self):
        # Facem threadul care tine tabla updatata
        threading = Thread(target=self.update_gui)
        threading.start()

    def update_gui(self):
        global x_click, y_click, click_event
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
                        click_event.set()
                    elif event.type == pygame.QUIT:
                        end = True
                        click_event.set()

                    # desenam detaliile tablei(fundalul, liniiile intre piese_tablale pieselor si piesele
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
        global coord_arr
        # 700 / 14 (13 coloane) = 50
        self.scala_imaginii = 50
        self.raza_piesa = 30
        self.culoare_jucator1 = (50, 140, 50)
        self.culoare_jucator2 = (30, 30, 90)
        self.window.fill((160, 160, 150))  # culoarea de fundal al tablei
        # trasam liniile intre piese_tablale pieselor
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
                    pygame.draw.circle(surface=self.window, color=self.culoare_jucator1,
                                       center=[x * self.scala_imaginii for x in centrul_pozitiei],
                                       radius=self.raza_piesa)
                else:
                    pygame.draw.circle(surface=self.window, color=self.culoare_jucator2,
                                       center=[x * self.scala_imaginii for x in centrul_pozitiei],
                                       radius=self.raza_piesa)

    def trage_linie(self, start, end, culoare_linii=(0, 0, 0), grosimea_liniei=8):
        pygame.draw.line(surface=self.window, color=culoare_linii,
                         start_pos=[x * self.scala_imaginii for x in start],
                         end_pos=[x * self.scala_imaginii for x in end],
                         width=grosimea_liniei)

    def afisare_tabla(self):
        result = ""
        # consideram X jucatorul 1 si 0 jucatorul 2

        # linia 1
        result += str(self.piese_tabla[0])
        for i in range(5):
            result += "-"
        result += str(self.piese_tabla[1])
        for i in range(5):
            result += "-"
        result += str(self.piese_tabla[2])
        result += "\n"

        # linia 2
        for i in range(13):
            if i in (0, 6, 12):
                result += "|"
            else:
                result += " "
        result += "\n"

        # linia 3
        result += "|"
        result += " "
        result += str(self.piese_tabla[3])
        for i in range(3):
            result += "-"
        result += str(self.piese_tabla[4])
        for i in range(3):
            result += "-"
        result += str(self.piese_tabla[5])
        result += " "
        result += "|"
        result += "\n"

        # linia 4
        result += "|"
        result += " "
        result += "|"
        for i in range(3):
            result += " "
        result += "|"
        for i in range(3):
            result += " "
        result += "|"
        result += " "
        result += "|"
        result += "\n"

        # linia 5
        result += "|"
        result += " "
        result += "|"
        result += " "
        result += str(self.piese_tabla[6])
        result += "-"
        result += str(self.piese_tabla[7])
        result += "-"
        result += str(self.piese_tabla[8])
        result += " "
        result += "|"
        result += " "
        result += "|"
        result += "\n"

        # linia 6
        for i in range(3):
            result += "| "
        for i in range(2):
            result += " "
        result += "|"
        for i in range(2):
            result += " |"
        result += "\n"

        # linia 7
        result += str(self.piese_tabla[9])
        result += "-"
        result += str(self.piese_tabla[10])
        result += "-"
        result += str(self.piese_tabla[11])
        for i in range(3):
            result += " "
        result += str(self.piese_tabla[12])
        result += "-"
        result += str(self.piese_tabla[13])
        result += "-"
        result += str(self.piese_tabla[14])
        result += "\n"

        # linia 8
        for i in range(2):
            result += "| "
        result += "|"
        for i in range(3):
            result += " "
        result += "|"
        for i in range(2):
            result += " |"
        result += "\n"

        # linia 9
        result += "|"
        result += " "
        result += "|"
        result += " "
        result += str(self.piese_tabla[15])
        result += "-"
        result += str(self.piese_tabla[16])
        result += "-"
        result += str(self.piese_tabla[17])
        result += " "
        result += "|"
        result += " "
        result += "|"
        result += "\n"

        # linia 10
        result += "|"
        result += " "
        result += "|"
        for i in range(3):
            result += " "
        result += "|"
        for i in range(3):
            result += " "
        result += "|"
        result += " "
        result += "|"
        result += "\n"

        # linia 11
        result += "|"
        result += " "
        result += str(self.piese_tabla[18])
        for i in range(3):
            result += "-"
        result += str(self.piese_tabla[19])
        for i in range(3):
            result += "-"
        result += str(self.piese_tabla[20])
        result += " "
        result += "|"
        result += "\n"

        # linia 12
        for i in range(13):
            if i in (0, 6, 12):
                result += "|"
            else:
                result += " "
        result += "\n"

        # linia 13
        result += str(self.piese_tabla[21])
        for i in range(5):
            result += "-"
        result += str(self.piese_tabla[22])
        for i in range(5):
            result += "-"
        result += str(self.piese_tabla[23])
        result += "\n"

        return result

    def get_pos_tabla_from_click(self):
        global x_click, y_click, click_event, coord_arr

        if x_click == y_click == 0:
            click_event.wait()

        x_click_aux = x_click
        y_click_aux = y_click

        x_click = y_click = 0
        click_event.clear()

        # print(f"x = {x_click_aux} || y = {y_click_aux}")  # DEBUG
        for index, (x, y) in enumerate(coord_arr):
            dx = x_click_aux - (x * self.scala_imaginii)
            dy = y_click_aux - (y * self.scala_imaginii)
            dist = math.pow(dx, 2) + math.pow(dy, 2)
            # x^2 + y^2 <= r^2->punctele de coord x,y care satisfac <= r^2 sunt in cerc
            if dist <= math.pow(self.raza_piesa, 2):
                # print("click in piesa: ", index + 1) # debug
                return index
        return -1

    def pos_empty(self, index_pos_piesa_apasata):
        if self.piese_tabla[index_pos_piesa_apasata] == 0:
            return True
        else:
            return False

    def get_index_sus(self, index):
        return above_arr[index]

    def get_index_jos(self, index):
        try:
            return above_arr.index(index)
        except ValueError:
            return -1

    def get_index_stanga(self, index):
        if index == -1:
            return -1
        if index % 3 == 0:
            return -1
        else:
            return index - 1

    def get_index_dreapta(self, index):
        if index == -1:
            return -1
        if index % 3 == 2:
            return -1
        else:
            return index + 1

    def pozitii_valide_mutare(self, index):
        return [self.get_index_dreapta(index), self.get_index_stanga(index),
                self.get_index_sus(index), self.get_index_jos(index)]

    def pune_piesa(self, jucator):
        # indexul pos  pieselor unde a fost facut click-ul, -1 daca este pos invalida
        index_pos = self.get_pos_tabla_from_click()
        # verific daca este o pozitie valida
        if index_pos == -1:
            print("Pozitia nu a fost gasita")
            return self.pune_piesa(jucator)
        elif not self.pos_empty(index_pos):
            print(f"Pozitia {index_pos} este ocupata")
            return self.pune_piesa(jucator)
        else:
            self.piese_tabla[index_pos] = jucator
            print("Piesa a fost pusa cu succes") # debug

            # verificam daca piesa pusa formeaza o moara
            if self.check_moara(index_pos, jucator):
                print("Piesa formeaza o moara")
                self.sterge_piesa(jucator * (-1))

    def muta_piesa(self, jucator, get_start=True, index_pos_start=-1):
        # selectam piesa pe care vrem sa o mutam
        if get_start:
            index_pos_start = self.get_pos_tabla_from_click()
            if index_pos_start == -1:
                print("Pozitia nu a fost gastia")
                return self.muta_piesa(jucator)
            elif self.pos_empty(index_pos_start):
                print("Pozitia selectata este goala")
                return self.muta_piesa(jucator)
            elif self.piese_tabla[index_pos_start] != jucator:
                print("Piesa selectata este a jucatorului advers")
                return self.muta_piesa(jucator)
            else:
                print("Selectati pozitia unde vrei sa fie mutata piesa")

        # selectam pozitia unde vrem sa o punem
        index_pos_mutare = self.get_pos_tabla_from_click()

        if index_pos_mutare == -1:
            print("Pozitia finala nu a fost gastia")
            return self.muta_piesa(jucator, False, index_pos_start)
        elif index_pos_start == index_pos_mutare:
            print("Mutarea a fost anulata, repetati")
            return self.muta_piesa(jucator)
        elif not self.pos_empty(index_pos_mutare):
            print("Pozitia selectata nu este goala")
            return self.muta_piesa(jucator, False, index_pos_start)
        elif index_pos_start == index_pos_mutare:
            print("Mutarea a fost anulata, repetati")
            return self.muta_piesa(jucator)
        elif index_pos_mutare not in self.pozitii_valide_mutare(index_pos_start):
            print("Mutare invalida")
            return self.muta_piesa(jucator, False, index_pos_start)
        else:
            # pozitiile sunt valide
            self.piese_tabla[index_pos_start] = 0
            self.piese_tabla[index_pos_mutare] = jucator

            print("Piesa a fost mutata")
            # verificam daca piesa mutata formeaza o moara
            if self.check_moara(index_pos_mutare, jucator):
                print("Piesa formeaza o moara")
                self.sterge_piesa(jucator * (-1))

    def sterge_piesa(self, inamic):
        print("Alegeti piesa inamicului pe care vreti sa o stergeti")
        index_pos = self.get_pos_tabla_from_click()

        if index_pos == -1:
            print("Pozitia nu a fost gasita")
            return self.sterge_piesa(inamic)
        elif self.piese_tabla[index_pos] != inamic:
            print("Puteti sterge doar piesele inamicului")
            return self.sterge_piesa(inamic)
        else:
            print("Piesa a fost stearsa")
            if inamic == self.JMIN:
                self.JMIN_num_piese -= 1
            else:
                self.JMAX_num_piese -= 1
            self.piese_tabla[index_pos] = 0

    def check_moara(self, index_mutare, jucator):
        # daca pe rand sau coloana sunt 3 piese alaturate

        # linie
        # verific daca piesa este in dreapta
        if self.get_index_stanga(index_mutare) != -1 and self.piese_tabla[index_mutare - 1] == jucator and \
                self.get_index_stanga(index_mutare - 1) != -1 and self.piese_tabla[index_mutare - 2] == jucator:
            return True
        # verific daca piesa este in centru
        elif self.get_index_stanga(index_mutare) != -1 and self.piese_tabla[index_mutare - 1] == jucator and \
                self.get_index_dreapta(index_mutare) != -1 and self.piese_tabla[index_mutare + 1] == jucator:
            return True
        # verific daca piesa este in stanga
        elif self.get_index_dreapta(index_mutare) != -1 and self.piese_tabla[index_mutare + 1] == jucator and \
                self.get_index_dreapta(index_mutare + 1) != -1 and self.piese_tabla[index_mutare + 2] == jucator:
            return True
        # coloana
        # verific daca piesa este sus
        elif self.get_index_jos(index_mutare) != -1 and \
                self.piese_tabla[self.get_index_jos(index_mutare)] == jucator and \
                self.get_index_jos(self.get_index_jos(index_mutare)) != -1 and \
                self.piese_tabla[self.get_index_jos(self.get_index_jos(index_mutare))] == jucator:
            return True
        # verific daca piesa este in centru
        elif self.get_index_sus(index_mutare) != -1 and \
                self.piese_tabla[self.get_index_sus(index_mutare)] == jucator and \
                self.get_index_jos(index_mutare) != -1 and \
                self.piese_tabla[self.get_index_jos(index_mutare)] == jucator:
            return True
        # verific daca piesa este jos
        elif self.get_index_sus(index_mutare) != -1 and \
                self.piese_tabla[self.get_index_sus(index_mutare)] == jucator and \
                self.get_index_sus(self.get_index_sus(index_mutare)) != -1 and \
                self.piese_tabla[self.get_index_sus(self.get_index_sus(index_mutare))] == jucator:
            return True
        else:
            return False

    def check_castigator(self, jucator):
        # pentru ca un jucator sa castige trebuie ca :
        # celalalt jucator sa aiba mai putin de 2 piese
        #                   SAU
        # celalalt jucator sa nu mai poate faca nici o miscare

        if jucator == self.JMIN and self.JMAX_num_piese < 3:
            return True
        if jucator == self.JMAX and self.JMIN_num_piese < 3:
            return True

        # print("============")
        # for index, piese in enumerate(self.piese_tabla):
        #     print(f"index = {index} -> piesa={piese}")
        # print("============")
        numar_piese = 0
        # daca inamicul poate are o mutare valabila, inseamna ca nu este castigator
        for pos, piesa_jucator in enumerate(self.piese_tabla):
            if piesa_jucator == jucator * (-1):
                numar_piese = 0
                # daca toate 4 directiile sunt blocate => piesa blocata
                counter = 0
                poz_posibile = 4
                if self.get_index_stanga(pos) == -1:
                    poz_posibile -= 1
                elif self.piese_tabla[self.get_index_stanga(pos)] != 0:
                    counter += 1
                if self.get_index_dreapta(pos) == -1:
                    poz_posibile -= 1
                elif self.piese_tabla[self.get_index_dreapta(pos)] != 0:
                    counter += 1
                if self.get_index_sus(pos) == -1:
                    poz_posibile -= 1
                elif self.piese_tabla[self.get_index_sus(pos)] != 0:
                    counter += 1
                if self.get_index_jos(pos) == -1:
                    poz_posibile -= 1
                elif self.piese_tabla[self.get_index_jos(pos)] != 0:
                    counter += 1
                # print(f"index {pos}, poz_pos {poz_posibile} -> counter {counter}")  # debug
                if counter < poz_posibile:
                    return False
        if numar_piese == 0:
            return False
        else:
            return True

    def mutari_libere(self):
        pozitii_libere = []
        for index, valoare in enumerate(self.piese_tabla):
            if valoare == 0:
                pozitii_libere.append(index)
        return pozitii_libere

    def estimare_scor(self, depth, jucator):
        # numarul de mori formate
        scor = 0
        for index, valoare in enumerate(self.piese_tabla):
            if valoare == jucator:
                if self.check_moara(index, jucator):
                    scor += 1
        scor -= depth / 2
        return scor
