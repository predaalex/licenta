import cv2 as cv

img = cv.imread("resources/big_picture.jpg")
img = cv.resize(img, (0, 0), fx=0.3, fy=0.3)

low_color_player1 = (0, 50, 114)
high_color_player1 = (31, 255, 255)
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
mask_yellow_hsv = cv.inRange(img_hsv, low_color_player1, high_color_player1)
cv.imshow('img_initial', img)
cv.imshow('mask_yellow_hsv', mask_yellow_hsv)
cv.waitKey(0)
cv.destroyAllWindows()