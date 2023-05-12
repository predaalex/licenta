import math
import cv2 as cv
import numpy as np
import pygame
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from threading import Event
from threading import Thread
from PIL import Image
from joblib import load
from torch.autograd import Variable

x_click = 0
y_click = 0
configuratie_noua = None
GOOD_MATCH_PERCENT = 0.7
MAX_MATCHES = 1000
game_event = Event()

# global x_click, y_click, click_settings

# referinta la ce piese din array-ul piese_tabla au deasupra lor(lookup table)
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
                      (1, 7), (3, 7), (5, 7), (9, 7), (11, 7), (13, 7),
                      (5, 9), (7, 9), (9, 9),
                      (3, 11), (7, 11), (11, 11),
                      (1, 13), (7, 13), (13, 13)],
                     dtype=[('x', 'i4'), ('y', 'i4')])


def alignImages(im1, im2):
    # Convert images to grayscale
    im1Gray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
    im2Gray = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)

    # Detect AKAZE featyres and compute descriptors
    akaze = cv.AKAZE_create()
    keypoints1, descriptors1 = akaze.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = akaze.detectAndCompute(im2Gray, None)

    # Detect ORB features and compute descriptors.
    # sift = cv.xfeatures2d.SIFT_create(MAX_MATCHES)
    # keypoints1, descriptors1 = sift.detectAndCompute(im1Gray, None)
    # keypoints2, descriptors2 = sift.detectAndCompute(im2Gray, None)

    # orb = cv.ORB_create(MAX_MATCHES)
    # keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    # keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    # matcher = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    # matches = matcher.match(descriptors1, descriptors2, None)
    # matches = list(matches)

    bf = cv.BFMatcher(cv.NORM_L1, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = list(matches)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    # imMatches = cv.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    # cv.imshow("matches", imMatches)
    # cv.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # print(f"points1 = {points1.shape}")
    # print(f"points2 = {points2.shape}")
    # print(points1)

    if len(points1) >= 4:
        # Find homography
        h, mask = cv.findHomography(points1, points2, cv.RANSAC)

        # Use homography
        height, width, channels = im2.shape
        im1Reg = cv.warpPerspective(im1, h, (width, height))

        return im1Reg, h
    else:
        print("no keypoints matching")
        return im1, 0


def get_configuratie_camera():
    global configuratie_noua, game_event

    if configuratie_noua is None:
        game_event.wait()

    # print("get_configuratie_camera") # DEBUG

    configuratie_noua_aux = configuratie_noua
    configuratie_noua = None
    game_event.clear()

    return configuratie_noua_aux


class StareJoc:
    def __init__(self, tabla=None, GUI=True, parinte=None, index_move=None, camera=False):
        self.estimare = 0
        self.raza_piesa = 30
        self.scala_imaginii = 50
        self.culoare_jucator2 = None
        self.culoare_jucator1 = None
        self.piese_tabla = None
        self.JMAX_num_piese = None
        self.JMIN_num_piese = None
        self.JMIN = -1
        self.JMAX = 1
        self.window = None
        self.clock = None
        self.parinte = parinte
        self.index_move = index_move
        self.camera = camera
        self.end = False

        if self.camera:
            # Initializare camera
            self.video_image = cv.VideoCapture(0)  # 0 - fol camera defaul t | aceasta imagine va fi aliniata
            # importam modelul de clasificare
            self.model = load("model_clasificare_piesa.joblib")
            self.resnet_model = models.resnet18(pretrained=True)
            self.layer = self.resnet_model._modules.get('avgpool')
            self.resnet_model.eval()

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

        # Pornim threadul
        threading.start()

    def update_gui(self):
        global x_click, y_click, game_event, configuratie_noua

        # Initializam jocul
        pygame.init()
        self.window = pygame.display.set_mode(size=(700, 700))
        pygame.display.set_caption("Tintar -> Preda Alexandru-Florin")
        self.window.fill((160, 160, 150))  # culoarea de fundal al tablei
        self.clock = pygame.time.Clock()  # folosim pentru a seta refresh rate-ul

        # Setam un timer care va forta update-ul ferestrei la fiecare 50ms
        pygame.time.set_timer(pygame.USEREVENT, 50)

        while not self.end:
            try:
                for event in pygame.event.get():
                    if (not self.camera) and event.type == pygame.MOUSEBUTTONDOWN:
                        x_click, y_click = pygame.mouse.get_pos()
                        game_event.set()
                    elif self.camera and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # print("am apasat space") # DEBUG
                        configuratie_noua = self.get_configuratie_from_camera_screenshot()
                        # print(configuratie_noua)  # DEBUG
                        game_event.set()
                    elif event.type == pygame.QUIT:
                        self.end = True
                        game_event.set()
                    elif event.type == pygame.USEREVENT:
                        pygame.display.flip()

                    # desenam detaliile tablei(fundalul, liniiile intre piese_tablale pieselor si piesele
                    self.desenare_tabla()
                    # updatam imaginea
                    pygame.display.flip()
                    # setam refresh rate-ul
                    self.clock.tick(60)
            except pygame.event:
                pygame.quit()
        pygame.quit()

    def desenare_tabla(self):
        global coord_arr
        # 700 / 14 (13 coloane) = 50
        self.culoare_jucator1 = (50, 140, 50)
        self.culoare_jucator2 = (170, 70, 80)
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
        global x_click, y_click, game_event, coord_arr

        if x_click == y_click == 0:
            game_event.wait()

        x_click_aux = x_click
        y_click_aux = y_click

        x_click = y_click = 0
        game_event.clear()

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
        if self.end:
            return
        # indexul pos pieselor unde a fost facut click-ul, -1 daca este pos invalida
        index_pos = self.get_pos_tabla_from_click()
        # verific daca este o pozitie valida
        if index_pos == -1:
            if self.end:
                return
            print("Pozitia nu a fost gasita")
            return self.pune_piesa(jucator)
        elif not self.pos_empty(index_pos):
            print(f"Pozitia {index_pos} este ocupata")
            return self.pune_piesa(jucator)
        else:
            self.piese_tabla[index_pos] = jucator
            print("Piesa a fost pusa cu succes")

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
        scor -= depth
        return scor

    def get_configuratie_from_camera_screenshot(self):
        # print("get_configuratie_from_camera_screenshot")
        success, camera_frame = self.video_image.read()
        img_template = cv.imread("../resources/template_test3.jpg")
        img_template = cv.resize(img_template, (350, 350))
        # cv.imshow("camera frame", camera_frame)
        img_aliniata, h = alignImages(camera_frame, img_template)
        # cv.imshow("img_aliniata", img_aliniata)

        lista_imagini_pozitii = \
            [img_aliniata[0:50, 0:50, :], img_aliniata[0:50, 150:200, :], img_aliniata[0:50, 300:350, :],
             img_aliniata[45:95, 45:95, :], img_aliniata[45:95, 150:200, :], img_aliniata[45:95, 250:300, :],
             img_aliniata[90:140, 93:143, :], img_aliniata[90:140, 150:200, :], img_aliniata[90:140, 215:265, :],
             img_aliniata[150:200, 0:50, :], img_aliniata[150:200, 50:100, :], img_aliniata[150:200, 90:140, :],
             img_aliniata[150:200, 215:265, :], img_aliniata[150:200, 255:305, :], img_aliniata[145:200, 300:350, :],
             img_aliniata[210:260, 93:143, :], img_aliniata[210:260, 150:200, :], img_aliniata[210:260, 215:265, :],
             img_aliniata[255:305, 50:100, :], img_aliniata[255:305, 150:200, :], img_aliniata[255:305, 250:300, :],
             img_aliniata[300:350, 0:50, :], img_aliniata[300:350, 150:200, :], img_aliniata[300:350, 300:350, :]]
        configuratie_camera = []
        for img in lista_imagini_pozitii:
            label = self.model.predict(self.image_to_resnet_descriptors(img))
            # cv.imshow("img", img)  # DEBUG
            # print(label)
            if label == "pozitii_libere":
                configuratie_camera.append(0)
            elif label == "piese_verzi":
                configuratie_camera.append(1)
            elif label == "piese_portocalii":
                configuratie_camera.append(-1)
            else:
                print("EROARE -> PIESA DETECTATATA NU CORESPUNE MODELULUI")
            # cv.waitKey(0)  # DEBUG
        # cv.destroyWindow("img")  # DEBUG
        # print(configuratie_camera)  # DEBUG
        # cv.waitKey(0)
        # cv.destroyWindow("img_aliniata")
        # cv.destroyWindow("camera frame")
        return np.array(configuratie_camera)

    def image_to_resnet_descriptors(self, img):
        images = []

        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        to_tensor = transforms.ToTensor()
        scaler = transforms.Resize((50, 50))

        img_PIL = Image.fromarray(img)
        t_img = Variable(normalize(to_tensor(scaler(img_PIL))).unsqueeze(0))
        my_embedding = torch.zeros(512)

        def copy_data(m, i, o):
            my_embedding.copy_(o.data.reshape(o.data.size(1)))

        h = self.layer.register_forward_hook(copy_data)
        self.resnet_model(t_img)
        h.remove()
        my_embedding = my_embedding.numpy()

        images.append(my_embedding)

        images = np.array(images)

        return images
