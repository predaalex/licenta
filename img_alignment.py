import cv2 as cv
import numpy as np
import time

MAX_MATCHES = 1000
GOOD_MATCH_PERCENT = 0.7


def alignImages(im1, im2, str):
    # Convert images to grayscale
    im1Gray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
    im2Gray = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)

    # Detect AKAZE featyres and compute descriptors
    # akaze = cv.AKAZE_create()
    # keypoints1, descriptors1 = akaze.detectAndCompute(im1Gray, None)
    # keypoints2, descriptors2 = akaze.detectAndCompute(im2Gray, None)

    # Detect ORB features and compute descriptors.
    sift = cv.xfeatures2d.SIFT_create(nfeatures=MAX_MATCHES)
    keypoints1, descriptors1 = sift.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = sift.detectAndCompute(im2Gray, None)

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
    cv.imshow(f"matches{str}", imMatches)
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

        return im1Reg, len(matches)
    else:
        print("no keypoints matching")
        return im1, 0


video_image = cv.VideoCapture(0)  # 0 - fol camera default | aceasta imagine va fi aliniata
referinta_fisier_template = 'resources/template1.jpg'
referinta_fisier_template2 = 'resources/template2.jpg'

# imagine dupa care va fi aliniata imagine camerei
img_template = cv.imread(referinta_fisier_template, cv.IMREAD_COLOR)
img_template = cv.resize(img_template, None, fx=0.5, fy=0.5)

img_template2 = cv.imread(referinta_fisier_template2, cv.IMREAD_COLOR)
img_template2 = cv.resize(img_template2, None, fx=0.5, fy=0.5)

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
    img_aliniata1 = None
    img_aliniata2 = None

    try:
        img_aliniata1, nr_matches1 = alignImages(camera, img_template, "1")
        # mse1 = np.mean((img_template - img_aliniata1) ** 2)
        # print(f"mse1 = {mse1}")
        print(f"nr_matches1 = {nr_matches1}")

        img_aliniata2, nr_matches2 = alignImages(camera, img_template2, "2")
        # mse2 = np.mean((img_template2 - img_aliniata2) ** 2)
        # print(f"mse2 = {mse2}")
        print(f"nr_matches2 = {nr_matches2}")

        cv.imshow("img aliniata", img_aliniata1)
        cv.imshow("img aliniata2", img_aliniata2)

        if nr_matches1 > nr_matches2:
            cv.imshow("THE CHOSEN ONE", img_aliniata1)
            print(1)
        else:
            print(2)
            cv.imshow("THE CHOSEN ONE", img_aliniata2)

        print("=============")

    except:
        print("A avut loc o eroare la alinierea imaginii")

    # asteptam ca o tasta sa fie apasata
    key = cv.waitKey(0) & 0xFF

    if key == ord('q'):
        break

    # tin cont de numarul de fps-uri al imaginii
    if time.time() - t > 1:
        print(f"FPS:{fps}")
        t = time.time()
        fps = 0

# eliberez camera si inchid fereastra
video_image.release()
cv.destroyAllWindows()
