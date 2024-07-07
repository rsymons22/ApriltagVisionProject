import cv2 as cv

image_num = 0

while True:
    status, img = cv.VideoCapture(0).read()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,6), None)

    print(f"ret: {ret}")

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("success")
        cv.imwrite(f"img{image_num}.jpg", img)
        image_num += 1

    cv.imshow('img', img)
    if cv.waitKey(3000) == 13: break

cv.destroyAllWindows()
