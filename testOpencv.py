import cv2

img = cv2.imread("./20201020_11.jpg")
cap = cv2.VideoCapture("./GH050039_1.mp4")

cv2.imshow("img", img)

cv2.waitKey(0)


while True:
	ret, frame = cap.read()
	if not ret:
		break
	cv2.imshow("cap", frame)

	key = cv2.waitKey(0)
	if key == 27 :
		break

cv2.destroyAllWindows()