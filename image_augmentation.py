import cv2 as cv
import numpy as np
import time

MAX_MATCHES = 1000
GOOD_MATCH_PERCENT = 0.7


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
    imMatches = cv.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv.imshow("matches", imMatches)
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


######################################################################################

video_image = cv.VideoCapture(0)  # 0 - fol camera default | aceasta imagine va fi aliniata
referinta_fisier_template = "resources/template_test3.jpg"  # imagine dupa care va fi aliniata imagine camerei
img_template = cv.imread(referinta_fisier_template, cv.IMREAD_COLOR)
img_template = cv.resize(img_template, (350, 350))
# cv.imshow("imRef", imRef)
# cv.waitKey(0)
# cv.destroyAllWindows()

index_piese_verzi = 0
index_piese_portocalii = 0
index_pozitii_libere = 0

# verific daca camera s-a deschis cu succes
if not video_image.isOpened():
    print("Cannot open camera")
    exit()

t = time.time()
fps = 0
# capturez continuu imaginea camerei
while True:
    fps += 1
    success, camera = video_image.read()
    cv.imshow("video", camera)
    img_aliniata = None

    try:
        img_aliniata, h = alignImages(camera, img_template)
        cv.imshow("img aliniata", img_aliniata)
    except:
        print("A avut loc o eroare la alinierea tablei")

    # low_color_player1 = (0, 50, 114)
    # high_color_player1 = (31, 255, 255)
    # img_hsv = cv.cvtColor(img_aliniata, cv.COLOR_BGR2HSV)
    # img_filtrata = cv.inRange(img_hsv, low_color_player1, high_color_player1)
    # cv.imshow("img_filtrata", img_filtrata)

    # asteptam ca o tasta sa fie apasata
    key = cv.waitKey(1) & 0xFF

    # verific daca space-ul este apasat pentru a detecta configuratia tablei
    if key == 32 and img_aliniata is not None:
        # Save the captured frame as a screenshot
        cv.imwrite("resources/screenshot.jpg", img_aliniata)
        print("Screenshot saved.")

        lista_imagini_pozitii = [img_aliniata[0:50, 0:50, :], img_aliniata[0:50, 150:200, :], img_aliniata[0:50, 300:350, :],
                                 img_aliniata[45:95, 45:95, :], img_aliniata[45:95, 150:200, :], img_aliniata[45:95, 250:300, :],
                                 img_aliniata[90:140, 93:143, :], img_aliniata[90:140, 150:200, :], img_aliniata[90:140, 215:265, :],
                                 img_aliniata[150:200, 0:50, :], img_aliniata[150:200, 50:100, :], img_aliniata[150:200, 90:140, :],
                                 img_aliniata[150:200, 215:265, :], img_aliniata[150:200, 255:305, :], img_aliniata[145:200, 300:350, :],
                                 img_aliniata[210:260, 93:143, :], img_aliniata[210:260, 150:200, :], img_aliniata[210:260, 215:265, :],
                                 img_aliniata[255:305, 50:100, :], img_aliniata[255:305, 150:200, :], img_aliniata[255:305, 250:300, :],
                                 img_aliniata[300:350, 0:50, :], img_aliniata[300:350, 150:200, :], img_aliniata[300:350, 300:350, :]]
        # DEBUG (vizualizare piese)
        save_path = "resources/img/"
        for index, img in enumerate(lista_imagini_pozitii):
            print(f"{index + 1} -> {img.shape}")
            cv.imshow(str(index + 1), img)
            key = cv.waitKey(0) & 0xFF
            if key == ord('1'):
                print("1")
                cv.imwrite(save_path + str(index_piese_verzi) + ".jpg", img)
                index_piese_verzi += 1
            elif key == ord('2'):
                print("2")
                cv.imwrite(save_path + str(index_piese_portocalii) + ".jpg", img)
                index_piese_portocalii += 1
            elif key == ord('3'):
                print("3")
                cv.imwrite(save_path + str(index_pozitii_libere) + ".jpg", img)
                index_pozitii_libere += 1
            else:
                print("tasta gresita")

            cv.destroyWindow(str(index + 1))
        print("end")

    # verific daca q-ul este apasat pentru a iesi din loop
    elif key == ord('q'):
        break

    # tin cont de numarul de fps-uri al imaginii
    if time.time() - t > 1:
        print(f"FPS:{fps}")
        t = time.time()
        fps = 0

# eliberez camera si inchid fereastra
video_image.release()
cv.destroyAllWindows()
