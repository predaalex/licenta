import cv2 as cv
import numpy as np
import time

MAX_MATCHES = 500
GOOD_MATCH_PERCENT = 0.8


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
    print(points1)

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

cap = cv.VideoCapture(0)  # 0 - fol camera default | aceasta imagine va fi aliniata
refFilename = "resources/template2.jpg"  # imagine dupa care va fi aliniata imagine camerei
imRef = cv.imread(refFilename, cv.IMREAD_COLOR)
imRef = cv.resize(imRef, (350, 350))
# cv.imshow("imRef", imRef)
# cv.waitKey(0)
# cv.destroyAllWindows()

# verific daca camera s-a deschis cu succes
if not cap.isOpened():
    print("Cannot open camera")
    exit()

t = time.time()
fps = 0
# capturez continuu imaginea camerei
while True:
    fps += 1
    success, camera = cap.read()
    cv.imshow("video", camera)
    imReg = None

    try:
        imReg, h = alignImages(camera, imRef)
        cv.imshow("img aliniata", imReg)
    except:
        print("A avut loc o eroare la alinierea tablei")

    # asteptam ca o tasta sa fie apasata
    key = cv.waitKey(1) & 0xFF

    # verific daca space-ul este apasat pentru a detecta configuratia tablei
    if key == 32 and imReg is not None:
        # Save the captured frame as a screenshot
        cv.imwrite("resources/screenshot.jpg", imReg)
        print("Screenshot saved.")

        lista_imagini_pozitii = [imReg[0:50, 0:50, :],      imReg[0:50, 150:200, :],    imReg[0:50, 300:350, :],
                                 imReg[50:90, 50:93, :],    imReg[50:90, 150:200, :],   imReg[50:90, 250:300, :],
                                 imReg[90:140, 93:143, :],  imReg[90:140, 150:200, :],  imReg[90:140, 215:265, :],
                                 imReg[145:200, 0:50, :],   imReg[145:200, 50:93, :],   imReg[145:200, 94:150, :],
                                 imReg[145:200, 220:260, :],imReg[145:200, 260:300, :], imReg[145:200, 301:350, :],
                                 imReg[210:260, 93:143, :], imReg[210:260, 150:200, :], imReg[210:260, 215:265, :],
                                 imReg[261:305, 50:93, :],  imReg[261:305, 150:200, :], imReg[261:305, 250:300, :],
                                 imReg[306:350, 0:50, :],   imReg[306:350, 150:200, :], imReg[306:350, 300:350, :]]
        for index, img in enumerate(lista_imagini_pozitii):
            cv.imshow(str(index), img)
            cv.waitKey(0)
            cv.destroyWindow(str(index))
        print("end")
        # im_prima_poz = imReg[0:50, 0:50, :]
        # im_a2a_poz = imReg[0:50, 150:200, :]
        # im_a3a_poz = imReg[0:50, 300:350, :]
        #
        # im_a4a_poz = imReg[50:90, 50:93, :]
        # im_a5a_poz = imReg[50:90, 150:200, :]
        # im_a6a_poz = imReg[50:90, 250:300, :]
        #
        # im_a7a_poz = imReg[90:140, 93:143, :]
        # im_a8a_poz = imReg[90:140, 150:200, :]
        # im_a9a_poz = imReg[90:140, 215:250, :]

        # im_a10a_poz = imReg[145:200, 0:50, :]
        # im_a11a_poz = imReg[145:200, 50:93, :]
        # im_a12a_poz = imReg[145:200, 94:144, :]

        # im_a13a_poz = imReg[145:200, 220:260, :]
        # im_a14a_poz = imReg[145:200, 260:300, :]
        # im_a15a_poz = imReg[145:200, 301:350, :]

        # im_a16a_poz = imReg[210:260, 93:143, :]
        # im_a17a_poz = imReg[210:260, 150:200, :]
        # im_a18a_poz = imReg[210:260, 215:250, :]

        # im_a19a_poz = imReg[261:305, 50:93, :]
        # im_a20a_poz = imReg[261:305, 150:200, :]
        # im_a21a_poz = imReg[261:305, 250:300, :]

        # im_a22a_poz = imReg[306:350, 0:50, :]
        # im_a23a_poz = imReg[306:350, 150:200, :]
        # im_a24a_poz = imReg[306:350, 300:350, :]


        cv.imshow("prima piesa", imReg[0:50, 0:40, :])
        cv.waitKey(0)
        cv.destroyWindow("prima piesa")

    # verific daca q-ul este apasat pentru a iesi din loop
    elif key == ord('q'):
        break

    # tin cont de numarul de fps-uri al imaginii
    if time.time() - t > 1:
        print(f"FPS:{fps}")
        t = time.time()
        fps = 0

# eliberez camera si inchid fereastra
cap.release()
cv.destroyAllWindows()
