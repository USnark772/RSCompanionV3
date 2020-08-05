import cv2

cap = cv2.VideoCapture(0)
for i in range(300):
    ret, frame = cap.read()
    if ret:
        cv2.imshow("video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break