import cv2 as cv
import numpy as np
import time

MAX_MATCHES = 500
GOOD_MATCH_PERCENT = 0.5


def alignImages(im1, im2):
    # Convert images to grayscale
    im1Gray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
    im2Gray = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    sift = cv.xfeatures2d.SIFT_create(MAX_MATCHES)
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
    cv.imshow("matches", imMatches)
    # cv.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv.findHomography(points1, points2, cv.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv.warpPerspective(im1, h, (width, height))

    return im1Reg, h

######################################################################################

cap = cv.VideoCapture(0) # 0 - fol camera default | aceasta imagine va fi aliniata

refFilename = "template.jpg" # imagine dupa care va fi aliniata imagine camerei
imRef = cv.imread(refFilename, cv.IMREAD_COLOR)

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
    
    imReg, h = alignImages(camera, imRef)
    cv.imshow("img aliniata", imReg)

    # asteptam ca o tasta sa fie apasata
    key = cv.waitKey(1) & 0xFF

    # verific daca space-ul este apasat pentru a detecta configuratia tablei
    if key == 32:
        # Save the captured frame as a screenshot
        cv.imwrite("screenshot.jpg", imReg)
        print("Screenshot saved.")

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